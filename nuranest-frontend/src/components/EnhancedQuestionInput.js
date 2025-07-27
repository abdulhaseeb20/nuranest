import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles, Clock, TrendingUp } from 'lucide-react';

const EnhancedQuestionInput = ({ onSendMessage, isLoading, isConnected }) => {
  const [message, setMessage] = useState('');

  const [showSuggestions, setShowSuggestions] = useState(true);
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
      setShowSuggestions(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };



  const autoResizeTextarea = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  useEffect(() => {
    autoResizeTextarea();
  }, [message]);

  const suggestedQuestions = [
    {
      question: "What foods should I avoid during pregnancy?",
      icon: "🍎",
      category: "Nutrition"
    },
    {
      question: "How much weight should I gain during pregnancy?",
      icon: "⚖️",
      category: "Health"
    },
    {
      question: "What exercises are safe during pregnancy?",
      icon: "🏃‍♀️",
      category: "Fitness"
    },
    {
      question: "When should I start taking prenatal vitamins?",
      icon: "💊",
      category: "Supplements"
    },
    {
      question: "What are the signs of labor?",
      icon: "👶",
      category: "Labor"
    },
    {
      question: "How can I manage morning sickness?",
      icon: "🤢",
      category: "Symptoms"
    }
  ];

  const quickActions = [
    { label: "Nutrition Guide", icon: "🥗" },
    { label: "Exercise Tips", icon: "💪" },
    { label: "Safety Checklist", icon: "✅" },
    { label: "Symptom Tracker", icon: "📊" }
  ];

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Quick Actions */}
      {!isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <h3 className="text-sm font-medium text-gray-600 mb-3 flex items-center gap-2">
            <Sparkles size={16} className="text-primary-500" />
            Quick Actions
          </h3>
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onSendMessage(`Tell me about ${action.label.toLowerCase()}`)}
                disabled={isLoading}
                className="px-4 py-2 text-sm bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <span>{action.icon}</span>
                <span>{action.label}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Suggested Questions */}
      {showSuggestions && !isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <h3 className="text-sm font-medium text-gray-600 mb-3 flex items-center gap-2">
            <TrendingUp size={16} className="text-secondary-500" />
            Popular Questions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {suggestedQuestions.map((item, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => onSendMessage(item.question)}
                disabled={isLoading}
                className="p-4 text-left bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{item.icon}</span>
                  <div className="flex-1">
                    <p className="text-sm text-gray-900 font-medium">{item.question}</p>
                    <p className="text-xs text-gray-500 mt-1">{item.category}</p>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Input Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative"
      >
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-4">
            <div className="flex items-end gap-3">
              <div className="flex-1 relative">
                <textarea
                  ref={textareaRef}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about pregnancy health..."
                  disabled={isLoading || !isConnected}
                  className="w-full px-4 py-3 border-0 resize-none focus:outline-none focus:ring-0 text-gray-900 placeholder-gray-400 min-h-[60px] max-h-32"
                  rows="1"
                />
              </div>
              
              <motion.button
                type="submit"
                disabled={!message.trim() || isLoading || !isConnected}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 min-w-[120px] justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Send size={16} />
                    <span>Send</span>
                  </>
                )}
              </motion.button>
            </div>
          </div>
        </form>
      </motion.div>

      {/* Connection Status */}
      {!isConnected && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-full text-sm">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span>Not connected to AI service</span>
          </div>
        </motion.div>
      )}

      {/* Processing Status */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">
            <Clock size={14} className="animate-spin" />
            <span>AI is processing your question...</span>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default EnhancedQuestionInput; 