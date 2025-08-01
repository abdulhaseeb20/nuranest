import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Bot, Clock, CheckCircle, Copy, ThumbsUp, ThumbsDown, Share2, BookOpen } from 'lucide-react';

const EnhancedChatMessage = ({ message, isUser, timestamp, processingTime, confidenceScore, sources }) => {
  const [showSources, setShowSources] = useState(false);
  const [copied, setCopied] = useState(false);

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatConfidence = (score) => {
    if (!score) return null;
    const percentage = Math.round(score * 100);
    let color = 'text-green-600';
    let bgColor = 'bg-green-100';
    if (percentage < 70) {
      color = 'text-yellow-600';
      bgColor = 'bg-yellow-100';
    }
    if (percentage < 50) {
      color = 'text-red-600';
      bgColor = 'bg-red-100';
    }
    
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${bgColor} ${color}`}>
        <CheckCircle size={12} />
        <span>{percentage}% confident</span>
      </div>
    );
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  const handleFeedback = (type) => {
    // TODO: Implement feedback system
    console.log(`Feedback: ${type}`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {!isUser && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center shadow-lg"
        >
          <Bot size={18} className="text-white" />
        </motion.div>
      )}
      
      <div className={`max-w-4xl ${isUser ? 'order-first' : ''}`}>
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`relative rounded-2xl shadow-lg ${
            isUser 
              ? 'bg-gradient-to-br from-primary-500 to-primary-600 text-white' 
              : 'bg-white text-gray-800 border border-gray-200'
          }`}
        >
          {/* Message Content */}
          <div className="p-6">
            <div className="whitespace-pre-wrap leading-relaxed">{message}</div>
            
            {/* AI Message Features */}
            {!isUser && (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <Clock size={12} />
                      <span>{formatTime(timestamp)}</span>
                    </div>
                    {processingTime && (
                      <span>• {processingTime.toFixed(1)}s</span>
                    )}
                  </div>
                  {formatConfidence(confidenceScore)}
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons for AI Messages */}
          {!isUser && (
            <div className="px-6 pb-4">
              <div className="flex items-center gap-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg transition-colors"
                  title="Copy response"
                >
                  <Copy size={12} />
                  {copied ? 'Copied!' : 'Copy'}
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleFeedback('positive')}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs bg-green-100 hover:bg-green-200 text-green-600 rounded-lg transition-colors"
                  title="Helpful response"
                >
                  <ThumbsUp size={12} />
                  Helpful
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleFeedback('negative')}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs bg-red-100 hover:bg-red-200 text-red-600 rounded-lg transition-colors"
                  title="Not helpful"
                >
                  <ThumbsDown size={12} />
                  Not Helpful
                </motion.button>

                {sources && sources.length > 0 && (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowSources(!showSources)}
                    className="flex items-center gap-1 px-3 py-1.5 text-xs bg-blue-100 hover:bg-blue-200 text-blue-600 rounded-lg transition-colors"
                    title="View sources"
                  >
                    <BookOpen size={12} />
                    Sources
                  </motion.button>
                )}

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {/* TODO: Implement share */}}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs bg-purple-100 hover:bg-purple-200 text-purple-600 rounded-lg transition-colors"
                  title="Share response"
                >
                  <Share2 size={12} />
                  Share
                </motion.button>
              </div>
            </div>
          )}
        </motion.div>

        {/* Sources Section */}
        <AnimatePresence>
          {showSources && sources && sources.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 bg-gray-50 rounded-lg p-4"
            >
              <h4 className="text-sm font-medium text-gray-900 mb-3">Sources:</h4>
              <div className="space-y-2">
                {sources.map((source, index) => (
                  <div key={index} className="text-xs text-gray-600 bg-white p-2 rounded border">
                    {source}
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {isUser && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-secondary-500 to-secondary-600 rounded-full flex items-center justify-center shadow-lg"
        >
          <User size={18} className="text-white" />
        </motion.div>
      )}
    </motion.div>
  );
};

export default EnhancedChatMessage; 