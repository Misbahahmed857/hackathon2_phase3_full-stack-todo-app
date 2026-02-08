'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Function to send messages to the AI
  const sendMessage = async () => {
    const inputElement = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');
    const token = localStorage.getItem('token');

    if (!inputElement || !messagesContainer || !token) return;

    const message = inputElement.value.trim();
    if (!message) return;

    // Add user message to chat
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'mb-4 flex justify-end';
    userMessageDiv.innerHTML = `
      <div class="bg-indigo-600 text-white p-3 rounded-lg max-w-[80%]">
        <p>${message}</p>
        <p class="text-xs opacity-75 mt-1 text-right">Just now</p>
      </div>
    `;
    messagesContainer.appendChild(userMessageDiv);

    // Clear input
    inputElement.value = '';

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Add "AI thinking" indicator
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = 'ai-thinking';
    thinkingDiv.className = 'mb-4 flex justify-start';
    thinkingDiv.innerHTML = `
      <div class="bg-gray-100 text-gray-600 p-3 rounded-lg max-w-[80%] flex items-center space-x-2">
        <div class="flex space-x-1">
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
        </div>
        <p class="text-sm">AI is thinking...</p>
      </div>
    `;
    messagesContainer.appendChild(thinkingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
      // Get user ID from token
      const tokenParts = token.split('.');
      let userId = null;
      if (tokenParts.length === 3) {
        const payload = JSON.parse(atob(tokenParts[1]));
        userId = payload.sub || payload.userId || payload.id;
      }

      if (!userId) {
        throw new Error('Could not extract user ID from token');
      }

      // Send message to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: {
            content: message,
            role: 'user'
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const responseData = await response.json();

      // Remove thinking indicator
      const thinkingIndicator = document.getElementById('ai-thinking');
      if (thinkingIndicator) {
        thinkingIndicator.remove();
      }

      // Add AI response to chat
      const aiMessageDiv = document.createElement('div');
      aiMessageDiv.className = 'mb-4 flex justify-start';
      aiMessageDiv.innerHTML = `
        <div class="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-[80%]">
          <p>${responseData.message.content}</p>
          <p class="text-xs opacity-75 mt-1">AI Assistant • Just now</p>
        </div>
      `;
      messagesContainer.appendChild(aiMessageDiv);

      // Scroll to bottom
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch (error) {
      console.error('Error sending message:', error);

      // Remove thinking indicator
      const thinkingIndicator = document.getElementById('ai-thinking');
      if (thinkingIndicator) {
        thinkingIndicator.remove();
      }

      // Add error message to chat
      const errorMessageDiv = document.createElement('div');
      errorMessageDiv.className = 'mb-4 flex justify-start';
      errorMessageDiv.innerHTML = `
        <div class="bg-red-100 text-red-800 p-3 rounded-lg max-w-[80%]">
          <p>Sorry, I encountered an error processing your request. Please try again.</p>
        </div>
      `;
      messagesContainer.appendChild(errorMessageDiv);

      // Scroll to bottom
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Get user info
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      setUser(data);
      setLoading(false);
    })
    .catch(err => {
      console.error('Error fetching user:', err);
      localStorage.removeItem('token');
      router.push('/login');
    });

    // Get tasks
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/tasks`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      setTasks(Array.isArray(data) ? data : []);
    })
    .catch(err => {
      console.error('Error fetching tasks:', err);
    });
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user?.email || 'User'}!</span>
            <button
              onClick={handleLogout}
              className="ml-4 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md transition duration-150 ease-in-out"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            {/* Create Task Button - Positioned on right side of main content */}
            <button
              onClick={() => document.getElementById('createTaskModal').classList.remove('hidden')}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md flex items-center transition-colors duration-200"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Create Task
            </button>
          </div>
          <div className="px-4 py-6 sm:px-0">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                      <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">Total Tasks</dt>
                        <dd className="text-2xl font-semibold text-gray-900">{tasks.length}</dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

            </div>


            {/* Tasks Section */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Your Tasks</h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">Manage your tasks efficiently</p>
              </div>
              <div className="border-t border-gray-200">
                {tasks.length > 0 ? (
                  <ul className="divide-y divide-gray-200">
                    {tasks.map((task) => (
                      <li key={task.id} className="px-4 py-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <div className="text-sm font-medium text-gray-900 truncate">
                            {task.title}
                          </div>
                          <div className="ml-2 flex-shrink-0 flex">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              task.is_completed
                                ? 'bg-green-100 text-green-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {task.is_completed ? 'Completed' : 'Pending'}
                            </span>
                          </div>
                        </div>
                        <div className="mt-2 text-sm text-gray-500">
                          <p className="truncate">{task.description}</p>
                        </div>
                        <div className="mt-3 flex justify-end space-x-2">
                          <button
                            onClick={() => {
                              document.getElementById('editTaskTitle').value = task.title;
                              document.getElementById('editTaskDescription').value = task.description || '';
                              document.getElementById('editTaskIsCompleted').checked = task.is_completed;
                              document.getElementById('editTaskModal').dataset.taskId = task.id;
                              document.getElementById('editTaskModal').classList.remove('hidden');
                            }}
                            className="text-sm font-medium text-indigo-600 hover:text-indigo-900"
                          >
                            Edit
                          </button>
                          <button
                            onClick={async () => {
                              if (confirm('Are you sure you want to delete this task?')) {
                                const token = localStorage.getItem('token');
                                if (!token) return;

                                try {
                                  const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/tasks/${task.id}`, {
                                    method: 'DELETE',
                                    headers: {
                                      'Authorization': `Bearer ${token}`
                                    },
                                  });

                                  if (response.ok) {
                                    setTasks(tasks.filter(t => t.id !== task.id));
                                  } else {
                                    alert('Failed to delete task');
                                  }
                                } catch (error) {
                                  alert('Error deleting task');
                                }
                              }
                            }}
                            className="text-sm font-medium text-red-600 hover:text-red-900"
                          >
                            Delete
                          </button>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="px-4 py-12 text-center">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
                    <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Modal for creating task */}
      <div id="createTaskModal" className="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">Create New Task</h3>
            <button
              onClick={() => document.getElementById('createTaskModal').classList.add('hidden')}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={async (e) => {
            e.preventDefault();
            const formData = {
              title: e.target.title.value,
              description: e.target.description.value,
              is_completed: false  // New tasks are created as pending by default
            };

            const token = localStorage.getItem('token');
            if (!token) return;

            try {
              const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/tasks`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData),
              });

              if (response.ok) {
                const newTask = await response.json();
                setTasks([...tasks, newTask]);
                document.getElementById('createTaskModal').classList.add('hidden');
                // Reset form
                e.target.reset();
              } else {
                alert('Failed to create task');
              }
            } catch (error) {
              alert('Error creating task');
            }
          }}>
            <div className="mb-4">
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input
                type="text"
                id="title"
                name="title"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Task title"
              />
            </div>

            <div className="mb-4">
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                id="description"
                name="description"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Task description (optional)"
              ></textarea>
            </div>


            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => document.getElementById('createTaskModal').classList.add('hidden')}
                className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Create Task
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Modal for editing task */}
      <div id="editTaskModal" className="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">Edit Task</h3>
            <button
              onClick={() => document.getElementById('editTaskModal').classList.add('hidden')}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={async (e) => {
            e.preventDefault();
            const taskId = document.getElementById('editTaskModal').dataset.taskId;
            const formData = {
              title: e.target.title.value,
              description: e.target.description.value,
              is_completed: document.getElementById('editTaskIsCompleted').checked
            };

            const token = localStorage.getItem('token');
            if (!token) return;

            try {
              const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData),
              });

              if (response.ok) {
                const updatedTask = await response.json();
                setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
                document.getElementById('editTaskModal').classList.add('hidden');
              } else {
                alert('Failed to update task');
              }
            } catch (error) {
              alert('Error updating task');
            }
          }}>
            <div className="mb-4">
              <label htmlFor="editTaskTitle" className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input
                type="text"
                id="editTaskTitle"
                name="title"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Task title"
              />
            </div>

            <div className="mb-4">
              <label htmlFor="editTaskDescription" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                id="editTaskDescription"
                name="description"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Task description (optional)"
              ></textarea>
            </div>

            <div className="mb-4 flex items-center">
              <input
                id="editTaskIsCompleted"
                name="is_completed"
                type="checkbox"
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="editTaskIsCompleted" className="ml-2 block text-sm text-gray-900">Completed</label>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => document.getElementById('editTaskModal').classList.add('hidden')}
                className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Update Task
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Floating Chat Button */}
      <button
        id="chat-float-btn"
        onClick={() => {
          const chatWindow = document.getElementById('chat-window');
          if (chatWindow) {
            chatWindow.classList.toggle('hidden');
          }
        }}
        className="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg z-50 transition-transform duration-300 transform hover:scale-105"
        aria-label="Open chat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>

      {/* Chat Window - Hidden by default */}
      <div id="chat-window" className="hidden fixed bottom-20 right-6 w-80 h-96 bg-white rounded-lg shadow-xl z-50 flex flex-col border border-gray-200">
        <div className="bg-indigo-600 text-white p-3 rounded-t-lg flex justify-between items-center">
          <h3 className="font-medium">AI Assistant</h3>
          <button
            onClick={() => document.getElementById('chat-window').classList.add('hidden')}
            className="text-white hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        <div id="chat-messages" className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <div className="text-center text-gray-500 text-sm py-8">
            Start a conversation with the AI assistant
          </div>
        </div>
        <div className="border-t border-gray-200 p-3 bg-white">
          <div className="flex">
            <input
              id="chat-input"
              type="text"
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 rounded-l-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  sendMessage();
                }
              }}
            />
            <button
              onClick={sendMessage}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-r-lg text-sm transition duration-150"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}