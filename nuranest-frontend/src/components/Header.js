import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Github, ExternalLink, Wifi, WifiOff } from 'lucide-react';

const Header = ({ isConnected, onToggleConnection }) => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-3"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
              <Heart className="w-6 h-6 text-white" fill="currentColor" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Nuranest</h1>
              <p className="text-xs text-gray-500">Pregnancy Health AI</p>
            </div>
          </motion.div>

          {/* Connection Status */}
          <div className="flex items-center gap-4">
            <button
              onClick={onToggleConnection}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isConnected
                  ? 'bg-green-100 text-green-700 hover:bg-green-200'
                  : 'bg-red-100 text-red-700 hover:bg-red-200'
              }`}
            >
              {isConnected ? (
                <>
                  <Wifi size={16} />
                  <span>Connected</span>
                </>
              ) : (
                <>
                  <WifiOff size={16} />
                  <span>Disconnected</span>
                </>
              )}
            </button>

            {/* Navigation Links */}
            <div className="flex items-center gap-2">
              <motion.a
                href="https://github.com/your-username/nuranest"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="View on GitHub"
              >
                <Github size={20} />
              </motion.a>
              
              <motion.a
                href="/api/docs"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                title="API Documentation"
              >
                <ExternalLink size={20} />
              </motion.a>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
};

export default Header; 