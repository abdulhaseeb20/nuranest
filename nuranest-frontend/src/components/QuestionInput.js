import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mic, MicOff } from 'lucide-react';

const QuestionInput = ({ onSendMessage, isLoading, isConnected }) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // TODO: Implement voice recording functionality
  };

  const suggestedQuestions = [
    "What foods should I avoid during pregnancy?",
    "How much weight should I gain during pregnancy?",
    "What exercises are safe during pregnancy?",
    "When should I start taking prenatal vitamins?",
    "What are the signs of labor?",
    "How can I manage morning sickness?"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Suggested Questions */}
      {!isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <h3 className="text-sm font-medium text-gray-600 mb-3">Suggested Questions:</h3>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onSendMessage(question)}
                disabled={isLoading}
                className="px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {question}
              </motion.button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about pregnancy health..."
              disabled={isLoading || !isConnected}
              className="input-field resize-none min-h-[60px] max-h-32 pr-12"
              rows="1"
            />
            <div className="absolute right-3 bottom-3 flex items-center gap-2">
              <button
                type="button"
                onClick={toggleRecording}
                disabled={isLoading || !isConnected}
                className="p-2 text-gray-400 hover:text-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                title="Voice input"
              >
                {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
              </button>
            </div>
          </div>
          
          <motion.button
            type="submit"
            disabled={!message.trim() || isLoading || !isConnected}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
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
      </form>

      {/* Connection Status */}
      {!isConnected && (
        <div className="mt-3 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span>Not connected to AI service</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionInput; 