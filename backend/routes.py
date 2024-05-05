# backend/routes.py

from flask import Blueprint, request, jsonify
from .models import Drone, Task, Image, db
import random
import string

health_bp = Blueprint('health', __name__, url_prefix='/api/health')
drones_bp = Blueprint('drones', __name__, url_prefix='/api/drones')
tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
images_bp = Blueprint('images', __name__, url_prefix='/api/images')

# sanity health check route

@health_bp.route('/', methods=['GET'])
def health():
    """
    Health check endpoint to verify the status of the service.
    
    Returns:
        A JSON response indicating the health status of the service.
        Status code 200 (OK) if the service is operational.
    """
    return jsonify({"status": "ok"}), 200


# Routes for Drone endpoint

@drones_bp.route('/', methods=['GET'])
def get_drones():
    """
    Retrieve a list of all drones available in the database.
    
    Returns:
        A JSON response containing a list of drones, each with its ID and name.
        Status code 404 (Not Found) if no drones are available.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        drones = Drone.query.all()
        if not drones:
            return jsonify({'message': 'No drones available'}), 404
        
        drone_list = [{'id': drone.id, 'name': drone.name} for drone in drones]
        return jsonify(drone_list)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@drones_bp.route('/', methods=['POST'])
def add_drone():
    """
    Add a new drone to the database.
    
    Request JSON format:
        {
            "name": "Drone Name"
        }
        
    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 201 (Created) if the drone is added successfully.
        Status code 400 (Bad Request) if required parameters are missing.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        data = request.json
        if not all(key in data for key in ['name']):
            return jsonify({'message': 'Missing required parameters'}), 400

        name = data['name']

        new_drone = Drone(name=name)
        db.session.add(new_drone)
        db.session.commit()

        return jsonify({'message': 'Drone added successfully', 'id': new_drone.id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@drones_bp.route('/<int:drone_id>', methods=['DELETE'])
def delete_drone(drone_id):
    """
    Delete a drone from the database by its ID.
    
    Args:
        drone_id: The ID of the drone to be deleted.
        
    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 200 (OK) if the drone is deleted successfully.
        Status code 404 (Not Found) if the drone does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        # Query the drone by ID
        drone = Drone.query.get(drone_id)
        if not drone:
            return jsonify({'message': 'Drone not found'}), 404
        
        # Delete the drone
        db.session.delete(drone)
        db.session.commit()

        return jsonify({'message': f'Drone with ID {drone_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Routes for Task endpoint

@tasks_bp.route('/', methods=['POST'])
def create_task():
    """
    Create a new task and associate it with a drone.
    
    Request JSON format:
        {
            "name": "Task Name",
            "description": "Task Description",
            "drone_id": 1  # ID of the associated drone
        }
    
    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 201 (Created) if the task is created successfully.
        Status code 400 (Bad Request) if required parameters are missing.
        Status code 404 (Not Found) if the associated drone does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        data = request.json
        if not all(key in data for key in ['name', 'drone_id']):
            return jsonify({'message': 'Missing required parameters'}), 400

        name = data['name']
        description = data.get('description', None)
        drone_id = data['drone_id']

        if not Drone.query.get(drone_id):
            return jsonify({'message': 'Drone does not exist'}), 404

        task = Task(name=name, description=description, drone_id=drone_id)
        db.session.add(task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/', methods=['GET'])
def get_all_tasks():
    """
    Retrieve a list of all tasks with their associated drones.
    
    Returns:
        A JSON response containing a list of tasks, each with its details and associated drone.
        Status code 404 (Not Found) if no tasks are available.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        tasks = Task.query.all()
        task_list = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'drone_id': task.drone_id,
                'drone_name': task.drone.name if task.drone else None,  # Handle if task has no associated drone
            }
            task_list.append(task_data)
        return jsonify(task_list)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retrieve a task by its ID along with details of its associated drone.
    
    Args:
        task_id: The ID of the task to retrieve.
        
    Returns:
        A JSON response containing the details of the specified task and its associated drone.
        Status code 404 (Not Found) if the task does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        task_data = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'drone_id': task.drone_id,
            'drone_name': task.drone.name,
        }
        return jsonify(task_data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """
    Execute a task by generating 5 random noisy images and associating them with the task.

    Args:
        task_id: The ID of the task to execute.

    Returns:
        A JSON response indicating the success or failure of the operation.
        If successful, returns a message indicating the task execution along with the generated image URLs.
        Status code 200 (OK) if the task is executed successfully.
        Status code 404 (Not Found) if the task does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        # Generate 5 random noisy images
        images = []
        for _ in range(5):
            image_url = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            image = Image(url=image_url, task_id=task.id)
            db.session.add(image)
            images.append(image_url)

        db.session.commit()

        return jsonify({'message': 'Task executed successfully', 'images': images}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task from the database by its ID.

    Args:
        task_id: The ID of the task to be deleted.

    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 200 (OK) if the task is deleted successfully.
        Status code 404 (Not Found) if the task does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update the details of a task in the database.

    Args:
        task_id: The ID of the task to be updated.

    Request JSON format:
        {
            "name": "Updated Task Name",
            "description": "Updated Task Description",
            "drone_id": 1  # Updated ID of the associated drone
        }

    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 200 (OK) if the task is updated successfully.
        Status code 404 (Not Found) if the task does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        data = request.json
        task.name = data.get('name', task.name)
        task.description = data.get('description', task.description)
        task.drone_id = data.get('drone_id', task.drone_id)

        db.session.commit()

        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@tasks_bp.route('/<int:task_id>/images', methods=['GET'])
def get_task_images(task_id):
    """
    Retrieve a list of images associated with a task.

    Args:
        task_id: The ID of the task to retrieve images for.

    Returns:
        A JSON response containing a list of image URLs associated with the specified task.
        Status code 404 (Not Found) if no images are found for the task.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Task not found'}), 404

        images = [{'id': image.id, 'url': image.url} for image in task.images]
        if not images:
            return jsonify({'message': 'No images found for this task'}), 404

        return jsonify(images)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Routes for Images endpoint

@images_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """
    Retrieve an image by its ID.
    
    Args:
        image_id: The ID of the image to retrieve.
        
    Returns:
        A JSON response containing the URL of the specified image.
        Status code 404 (Not Found) if the image does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        image = Image.query.get(image_id)
        if not image:
            return jsonify({'message': 'Image not found'}), 404

        return jsonify({'url': image.url})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@images_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """
    Delete an image by its ID.
    
    Args:
        image_id: The ID of the image to delete.
        
    Returns:
        A JSON response indicating the success or failure of the operation.
        Status code 200 (OK) if the image is deleted successfully.
        Status code 404 (Not Found) if the image does not exist.
        Status code 500 (Internal Server Error) if an unexpected error occurs.
    """
    try:
        image = Image.query.get(image_id)
        if not image:
            return jsonify({'message': 'Image not found'}), 404

        db.session.delete(image)
        db.session.commit()

        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Error handling for unsupported HTTP methods

@drones_bp.route('/', methods=['PUT'])
@tasks_bp.route('/', methods=['PUT', 'DELETE'])
@tasks_bp.route('/<int:task_id>', methods=['POST'])
@images_bp.route('/<int:image_id>', methods=['POST', 'PUT'])
def method_not_allowed():
    return jsonify({'message': 'Method not allowed for this endpoint'}), 405
