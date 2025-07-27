import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot, Clock, CheckCircle } from 'lucide-react';

const ChatMessage = ({ message, isUser, timestamp, processingTime, confidenceScore }) => {
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatConfidence = (score) => {
    if (!score) return null;
    const percentage = Math.round(score * 100);
    let color = 'text-green-600';
    if (percentage < 70) color = 'text-yellow-600';
    if (percentage < 50) color = 'text-red-600';
    
    return (
      <div className={`flex items-center gap-1 text-sm ${color}`}>
        <CheckCircle size={14} />
        <span>{percentage}% confident</span>
      </div>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
          <Bot size={16} className="text-primary-600" />
        </div>
      )}
      
      <div className={`max-w-3xl ${isUser ? 'order-first' : ''}`}>
        <div className={`chat-bubble ${isUser ? 'user-message' : 'ai-message'}`}>
          <div className="whitespace-pre-wrap">{message}</div>
          
          {!isUser && (
            <div className="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
              <div className="flex items-center gap-2">
                <Clock size={12} />
                <span>{formatTime(timestamp)}</span>
                {processingTime && (
                  <span>• {processingTime.toFixed(1)}s</span>
                )}
              </div>
              {formatConfidence(confidenceScore)}
            </div>
          )}
        </div>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-secondary-100 rounded-full flex items-center justify-center">
          <User size={16} className="text-secondary-600" />
        </div>
      )}
    </motion.div>
  );
};

export default ChatMessage; 