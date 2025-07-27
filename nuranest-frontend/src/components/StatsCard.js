import React from 'react';
import { motion } from 'framer-motion';
import { Clock, CheckCircle, Brain, TrendingUp } from 'lucide-react';

const StatsCard = ({ title, value, icon: Icon, color, trend, description }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 ${color} rounded-lg flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {trend && (
          <div className="flex items-center gap-1 text-green-600 text-sm">
            <TrendingUp size={16} />
            <span>{trend}</span>
          </div>
        )}
      </div>
      
      <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
      <p className="text-gray-600 font-medium mb-2">{title}</p>
      {description && (
        <p className="text-sm text-gray-500">{description}</p>
      )}
    </motion.div>
  );
};

const StatsSection = ({ totalQuestions, avgResponseTime, accuracy, activeUsers }) => {
  const stats = [
    {
      title: "Questions Answered",
      value: totalQuestions || "0",
      icon: Brain,
      color: "bg-gradient-to-br from-primary-500 to-primary-600",
      description: "Total AI interactions"
    },
    {
      title: "Avg Response Time",
      value: avgResponseTime || "1.2s",
      icon: Clock,
      color: "bg-gradient-to-br from-secondary-500 to-secondary-600",
      description: "Fast and efficient"
    },
    {
      title: "Accuracy Rate",
      value: accuracy || "95%",
      icon: CheckCircle,
      color: "bg-gradient-to-br from-green-500 to-green-600",
      description: "Evidence-based answers"
    },
    {
      title: "Active Users",
      value: activeUsers || "1",
      icon: TrendingUp,
      color: "bg-gradient-to-br from-purple-500 to-purple-600",
      description: "Trusted by many"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <StatsCard
          key={index}
          {...stat}
        />
      ))}
    </div>
  );
};

export default StatsSection; 