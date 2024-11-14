import React, { useState } from 'react';
import { Shield } from 'lucide-react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState<any[]>([]);

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Shield className="w-8 h-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">CyberViz Analytics</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {data.length === 0 ? (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900">Cyber Attack Analysis Dashboard</h1>
              <p className="mt-2 text-gray-600">
                Upload your CSV file to visualize and analyze cyber attack patterns
              </p>
            </div>
            <FileUpload onFileUpload={setData} />
          </div>
        ) : (
          <Dashboard data={data} />
        )}
      </main>
    </div>
  );
}

export default App;