import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster, toast } from 'react-hot-toast';
import { pregnancyAPI } from './services/api';
import Header from './components/Header';
import WelcomeMessage from './components/WelcomeMessage';
import EnhancedChatMessage from './components/EnhancedChatMessage';
import LoadingMessage from './components/LoadingMessage';
import EnhancedQuestionInput from './components/EnhancedQuestionInput';
import ThinkingProcess from './components/ThinkingProcess';
import StatsSection from './components/StatsCard';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [thinkingStep, setThinkingStep] = useState(0);
  const [showThinking, setShowThinking] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // Scroll to bottom whenever messages change
    setTimeout(() => {
      scrollToBottom();
    }, 100);
  }, [messages, showThinking]);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      setIsInitializing(true);
      const health = await pregnancyAPI.getHealth();
      console.log('✅ API Health Check:', health);
      setIsConnected(true);
      toast.success('Connected to Nuranest AI');
    } catch (error) {
      console.error('❌ API Connection Failed:', error);
      setIsConnected(false);
      toast.error('Failed to connect to AI service');
    } finally {
      setIsInitializing(false);
    }
  };

  const simulateThinkingProcess = () => {
    setShowThinking(true);
    setThinkingStep(1);
    
    const steps = [1, 2, 3, 4];
    steps.forEach((step, index) => {
      setTimeout(() => {
        setThinkingStep(step);
      }, (index + 1) * 800);
    });
  };

  const handleSendMessage = async (message) => {
    if (!message.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      message: message,
      isUser: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    simulateThinkingProcess();

    try {
      // Get AI response
      const response = await pregnancyAPI.askQuestion(message);
      
      // Clear thinking process first
      setShowThinking(false);
      setThinkingStep(0);
      
      const aiMessage = {
        id: Date.now() + 1,
        message: response.answer,
        isUser: false,
        timestamp: response.timestamp,
        processingTime: response.processing_time,
        confidenceScore: response.confidence_score,
        sources: response.sources || []
      };

      setMessages(prev => [...prev, aiMessage]);
      toast.success('Response received!');
    } catch (error) {
      console.error('Error getting AI response:', error);
      
      // Clear thinking process first
      setShowThinking(false);
      setThinkingStep(0);
      
      const errorMessage = {
        id: Date.now() + 1,
        message: `Sorry, I couldn't process your question right now. Please try again later. Error: ${error.message}`,
        isUser: false,
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to get response from AI');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleConnection = () => {
    checkConnection();
  };

  const clearChat = () => {
    setMessages([]);
    setShowThinking(false);
    setThinkingStep(0);
    toast.success('Chat cleared');
  };

  if (isInitializing) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"
          />
          <p className="text-gray-600">Connecting to Nuranest AI...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      <Header isConnected={isConnected} onToggleConnection={handleToggleConnection} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Welcome Message */}
          {messages.length === 0 && !isLoading && (
            <WelcomeMessage />
          )}

          {/* Chat Messages */}
          <div className="mb-8">
            <AnimatePresence>
              {messages.map((msg) => (
                <EnhancedChatMessage
                  key={msg.id}
                  message={msg.message}
                  isUser={msg.isUser}
                  timestamp={msg.timestamp}
                  processingTime={msg.processingTime}
                  confidenceScore={msg.confidenceScore}
                  sources={msg.sources}
                />
              ))}
            </AnimatePresence>
            
            {/* Loading Message */}
            {isLoading && !showThinking && <LoadingMessage />}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Thinking Process */}
          {showThinking && (
            <ThinkingProcess currentStep={thinkingStep} totalSteps={4} />
          )}

          {/* Clear Chat Button */}
          {messages.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center mb-6"
            >
              <button
                onClick={clearChat}
                className="text-sm text-gray-500 hover:text-gray-700 transition-colors px-4 py-2 rounded-lg hover:bg-white hover:shadow-sm"
              >
                Clear Chat
              </button>
            </motion.div>
          )}

          {/* Input Section */}
          <EnhancedQuestionInput
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            isConnected={isConnected}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm text-gray-500">
            © 2024 Nuranest. AI-powered pregnancy health assistant. 
            Always consult healthcare professionals for medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App; 