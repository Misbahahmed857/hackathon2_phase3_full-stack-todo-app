import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32">
            {/* Navigation */}
            <nav className="relative max-w-7xl mx-auto flex items-center justify-between pt-6 px-4 sm:px-6 lg:px-8">
              <div className="flex items-center">
                <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl shadow-md">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <span className="ml-3 text-xl font-display font-bold text-gray-900">TaskAI</span>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  href="/login"
                  className="text-gray-700 hover:text-primary-600 font-medium transition-colors"
                >
                  Sign in
                </Link>
                <Link
                  href="/register"
                  className="btn-primary"
                >
                  Get Started
                </Link>
              </div>
            </nav>

            {/* Hero Content */}
            <main className="mt-16 mx-auto max-w-7xl px-4 sm:mt-24 sm:px-6 lg:mt-32">
              <div className="text-center animate-fade-in">
                <h1 className="text-4xl tracking-tight font-display font-bold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block">Manage Tasks with</span>
                  <span className="block bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                    AI-Powered Intelligence
                  </span>
                </h1>
                <p className="mt-3 max-w-md mx-auto text-base text-gray-600 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                  Your smart task management assistant. Create, organize, and complete tasks naturally using AI. Boost your productivity with intelligent task management.
                </p>
                <div className="mt-10 flex justify-center space-x-4">
                  <Link
                    href="/register"
                    className="btn-primary text-lg px-8 py-3"
                  >
                    Start Free Trial
                  </Link>
                  <Link
                    href="/login"
                    className="btn-secondary text-lg px-8 py-3"
                  >
                    Sign In
                  </Link>
                </div>
              </div>
            </main>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-display font-bold text-gray-900">
                Everything you need to stay organized
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Powerful features to help you manage tasks efficiently
              </p>
            </div>

            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <div className="card p-6 text-center transform hover:scale-105 transition-transform duration-300">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-xl mb-4">
                  <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Assistant</h3>
                <p className="text-gray-600">Chat naturally with AI to manage your tasks effortlessly</p>
              </div>

              {/* Feature 2 */}
              <div className="card p-6 text-center transform hover:scale-105 transition-transform duration-300">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-secondary-100 rounded-xl mb-4">
                  <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Organization</h3>
                <p className="text-gray-600">Keep your tasks organized with intelligent categorization</p>
              </div>

              {/* Feature 3 */}
              <div className="card p-6 text-center transform hover:scale-105 transition-transform duration-300">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-success-100 rounded-xl mb-4">
                  <svg className="w-6 h-6 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Track Progress</h3>
                <p className="text-gray-600">Monitor your productivity and complete tasks efficiently</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}