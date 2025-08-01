import React from 'react';
import { motion } from 'framer-motion';
import { Bot } from 'lucide-react';

const LoadingMessage = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex gap-3 mb-4 justify-start"
    >
      <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
        <Bot size={16} className="text-primary-600" />
      </div>
      
      <div className="max-w-3xl">
        <div className="chat-bubble ai-message">
          <div className="flex items-center gap-2">
            <div className="flex space-x-1">
              <motion.div
                className="w-2 h-2 bg-primary-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
              />
              <motion.div
                className="w-2 h-2 bg-primary-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
              />
              <motion.div
                className="w-2 h-2 bg-primary-400 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
              />
            </div>
            <span className="text-gray-600 text-sm">AI is thinking...</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default LoadingMessage; 