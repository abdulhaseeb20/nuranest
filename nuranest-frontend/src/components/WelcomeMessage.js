import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Shield, Brain, MessageCircle } from 'lucide-react';

const WelcomeMessage = () => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered",
      description: "Advanced AI trained on pregnancy health data"
    },
    {
      icon: Shield,
      title: "Safe & Reliable",
      description: "Evidence-based information from trusted sources"
    },
    {
      icon: MessageCircle,
      title: "24/7 Support",
      description: "Get answers to your questions anytime"
    },
    {
      icon: Heart,
      title: "Personalized",
      description: "Tailored advice for your pregnancy journey"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="text-center max-w-4xl mx-auto mb-8"
    >
      <div className="mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-6"
        >
          <Heart className="w-10 h-10 text-white" fill="currentColor" />
        </motion.div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Nuranest
        </h1>
        <p className="text-xl text-gray-600 mb-6">
          Your AI-powered pregnancy health companion
        </p>
        <p className="text-gray-500 max-w-2xl mx-auto">
          Ask me anything about pregnancy, nutrition, exercise, symptoms, or any health concerns. 
          I'm here to provide evidence-based information and support your pregnancy journey.
        </p>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="card text-center"
          >
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <feature.icon className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
            <p className="text-sm text-gray-600">{feature.description}</p>
          </motion.div>
        ))}
      </div>

      {/* Disclaimer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto"
      >
        <p className="text-sm text-blue-800">
          <strong>Medical Disclaimer:</strong> This AI assistant provides general information for educational purposes only. 
          It is not a substitute for professional medical advice, diagnosis, or treatment. 
          Always consult with your healthcare provider for personalized medical guidance.
        </p>
      </motion.div>
    </motion.div>
  );
};

export default WelcomeMessage; 