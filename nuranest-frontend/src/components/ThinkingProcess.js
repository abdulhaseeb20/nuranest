import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Circle, Brain, Search, FileText, Sparkles } from 'lucide-react';

const ThinkingProcess = ({ currentStep, totalSteps = 4 }) => {
  const steps = [
    {
      id: 1,
      title: "Analyzing Question",
      description: "Understanding your pregnancy health question",
      icon: Brain,
      color: "text-blue-600"
    },
    {
      id: 2,
      title: "Searching Knowledge Base",
      description: "Finding relevant medical information",
      icon: Search,
      color: "text-purple-600"
    },
    {
      id: 3,
      title: "Processing Information",
      description: "Analyzing evidence-based data",
      icon: FileText,
      color: "text-green-600"
    },
    {
      id: 4,
      title: "Generating Response",
      description: "Creating personalized answer",
      icon: Sparkles,
      color: "text-pink-600"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 mb-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
          <Brain className="w-4 h-4 text-white" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900">AI Processing Steps</h3>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const isCompleted = currentStep > step.id;
          const isCurrent = currentStep === step.id;
          const Icon = step.icon;

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`flex items-start gap-4 p-3 rounded-lg transition-all duration-300 ${
                isCurrent 
                  ? 'bg-gradient-to-r from-primary-50 to-secondary-50 border border-primary-200' 
                  : isCompleted 
                    ? 'bg-green-50 border border-green-200' 
                    : 'bg-gray-50 border border-gray-200'
              }`}
            >
              <div className="flex-shrink-0 mt-1">
                {isCompleted ? (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 200 }}
                  >
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  </motion.div>
                ) : isCurrent ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  >
                    <Circle className="w-5 h-5 text-primary-600" />
                  </motion.div>
                ) : (
                  <Circle className="w-5 h-5 text-gray-400" />
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Icon className={`w-4 h-4 ${step.color}`} />
                  <h4 className={`font-medium ${
                    isCurrent ? 'text-primary-700' : 
                    isCompleted ? 'text-green-700' : 'text-gray-600'
                  }`}>
                    {step.title}
                  </h4>
                </div>
                <p className="text-sm text-gray-500">{step.description}</p>
                
                {isCurrent && (
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="mt-2 h-1 bg-gradient-to-r from-primary-400 to-secondary-400 rounded-full"
                  />
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>Progress: {Math.round((currentStep / totalSteps) * 100)}%</span>
          <span>Step {currentStep} of {totalSteps}</span>
        </div>
        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${(currentStep / totalSteps) * 100}%` }}
            transition={{ duration: 0.5 }}
            className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
          />
        </div>
      </div>
    </motion.div>
  );
};

export default ThinkingProcess; 