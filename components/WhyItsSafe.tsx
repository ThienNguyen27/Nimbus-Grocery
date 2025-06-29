import React from "react";

interface SafetyFeature {
  icon: string;
  title: string;
  description: string;
}

const safetyFeatures: SafetyFeature[] = [
  {
    icon: "🔐",
    title: "Biometric Encryption",
    description: "Face data is never stored — it's encrypted and verified on-device.",
  },
  {
    icon: "🧠",
    title: "Smart Fraud Detection",
    description: "AI-based anomaly detection prevents unauthorized use.",
  },
  {
    icon: "🌍",
    title: "Privacy by Design",
    description: "GDPR and CCPA-compliant architecture ensures privacy.",
  },
  {
    icon: "🛡️",
    title: "End-to-End Encryption",
    description: "Payments and identity are always protected.",
  },
];

const WhyItsSafe: React.FC = () => {
  return (
    <section className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-2xl">
      <h2 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-2">
        🔒 Why It's Safe
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {safetyFeatures.map((feature, index) => (
          <div
            key={index}
            className="bg-green-50 p-5 rounded-xl shadow-sm flex items-start space-x-4"
          >
            <div className="text-3xl">{feature.icon}</div>
            <div>
              <h3 className="font-semibold text-gray-900 text-lg">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default WhyItsSafe;
