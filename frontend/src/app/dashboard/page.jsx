'use client';

import React, { useState, useEffect } from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import { useAuth } from '../../components/AuthProvider/AuthProvider';
import { getTasks, createTask, updateTask, deleteTask } from '../../lib/api';

const DashboardPage = () => {
  const { logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await getTasks();
      setTasks(tasksData);
    } catch (err) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p>Loading tasks...</p>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-semibold text-gray-900">Task Manager</h1>
              </div>
              <div className="flex items-center">
                <button
                  onClick={handleLogout}
                  className="ml-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>

        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="lg:flex lg:items-center lg:justify-between">
              <div className="min-w-0 flex-1">
                <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                  My Tasks
                </h2>
              </div>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 p-4 mb-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            <div className="mt-6">
              <TaskList tasks={tasks} setTasks={setTasks} />
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

// TaskList Component
const TaskList = ({ tasks, setTasks }) => {
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [showForm, setShowForm] = useState(false);

  const handleCreateTask = async (e) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      alert('Task title is required');
      return;
    }

    try {
      const taskData = {
        title: newTaskTitle,
        description: newTaskDescription
      };

      const newTask = await createTask(taskData);
      setTasks(prev => [...prev, newTask]);

      // Reset form
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowForm(false);
    } catch (err) {
      alert('Failed to create task: ' + err.message);
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      const updatedTask = await updateTask(task.id, {
        ...task,
        is_completed: !task.is_completed
      });

      setTasks(prev => prev.map(t => t.id === task.id ? updatedTask : t));
    } catch (err) {
      alert('Failed to update task: ' + err.message);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await deleteTask(taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      alert('Failed to delete task: ' + err.message);
    }
  };

  return (
    <div>
      <div className="mb-6">
        {!showForm ? (
          <button
            onClick={() => setShowForm(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add New Task
          </button>
        ) : (
          <form onSubmit={handleCreateTask} className="mb-6 p-4 bg-white rounded-lg shadow">
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Task Title *
                </label>
                <input
                  type="text"
                  id="title"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Enter task title"
                  maxLength={200}
                  required
                />
                <p className="mt-1 text-xs text-gray-500">1-200 characters</p>
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  id="description"
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                  rows={3}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Enter task description (optional)"
                  maxLength={1000}
                />
                <p className="mt-1 text-xs text-gray-500">Max 1000 characters</p>
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Create Task
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Cancel
                </button>
              </div>
            </div>
          </form>
        )}
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              vectorEffect="non-scaling-stroke"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

// TaskItem Component
const TaskItem = ({ task, onToggleComplete, onDelete }) => {
  return (
    <li className="bg-white px-4 py-6 shadow sm:rounded-lg sm:p-6">
      <div className="flex items-start">
        <div className="flex items-center h-5">
          <input
            id={`task-${task.id}`}
            type="checkbox"
            checked={task.is_completed}
            onChange={() => onToggleComplete(task)}
            className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
          />
        </div>
        <div className="ml-3 min-w-0 flex-1">
          <label htmlFor={`task-${task.id}`} className="text-base font-medium text-gray-900">
            {task.title}
          </label>
          {task.description && (
            <p className="text-sm text-gray-500 mt-1">{task.description}</p>
          )}
          <div className="mt-2 flex items-center text-xs text-gray-500">
            <span>Created: {new Date(task.created_at).toLocaleString()}</span>
            <span className="mx-2">•</span>
            <span>Updated: {new Date(task.updated_at).toLocaleString()}</span>
          </div>
        </div>
        <div className="ml-4 flex-shrink-0">
          <button
            onClick={() => onDelete(task.id)}
            className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
};

export default DashboardPage;