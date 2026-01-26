import React, { useState } from 'react';
import TaskForm from '../TaskForm/TaskForm';

const TaskItem = ({ task, onUpdate, onDelete, onToggleComplete }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleUpdate = async (taskId, taskData) => {
    try {
      await onUpdate(taskId, taskData);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update task:', error);
      alert('Failed to update task: ' + error.message);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    onToggleComplete(task);
  };

  return (
    <div className="bg-white px-4 py-5 shadow sm:p-6 rounded-lg">
      {isEditing ? (
        <div className="mb-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Edit Task</h3>
          <TaskForm
            initialData={task}
            onSubmit={handleUpdate}
            onCancel={handleCancelEdit}
          />
        </div>
      ) : (
        <div className="flex items-start">
          <div className="flex items-center h-5">
            <input
              id={`task-${task.id}`}
              type="checkbox"
              checked={task.is_completed}
              onChange={handleToggleComplete}
              className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
            />
          </div>
          <div className="ml-3 min-w-0 flex-1">
            <h3
              className={`text-base font-medium ${
                task.is_completed ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-gray-500 mt-1">{task.description}</p>
            )}
            <div className="mt-2 flex items-center text-xs text-gray-500">
              <span>Created: {new Date(task.created_at).toLocaleString()}</span>
              <span className="mx-2">•</span>
              <span>Updated: {new Date(task.updated_at).toLocaleString()}</span>
            </div>
          </div>
          <div className="ml-4 flex space-x-2">
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;