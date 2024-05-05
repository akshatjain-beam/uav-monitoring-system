# backend/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drone(db.Model):
    """
    Model class representing a drone.

    Attributes:
        id (int): The unique identifier for the drone.
        name (str): The name of the drone.
        tasks (Relationship): One-to-many relationship with Task model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='drone', lazy=True)

class Task(db.Model):
    """
    Model class representing a task.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name of the task.
        description (str): The description of the task.
        drone_id (int): The ID of the associated drone.
        images (Relationship): One-to-many relationship with Image model.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drone.id'), nullable=False)
    images = db.relationship('Image', backref='task', lazy=True)

class Image(db.Model):
    """
    Model class representing an image captured during a task.

    Attributes:
        id (int): The unique identifier for the image.
        url (str): The URL of the image.
        task_id (int): The ID of the task associated with the image.
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
