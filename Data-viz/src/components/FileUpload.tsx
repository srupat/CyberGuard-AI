import React from 'react';
import { Upload } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (data: any[]) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      const text = e.target?.result;
      const Papa = (await import('papaparse')).default;
      const result = Papa.parse(text as string, { header: true });
      onFileUpload(result.data);
    };
    reader.readAsText(file);
  };

  return (
    <div className="w-full p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
      <label className="flex flex-col items-center cursor-pointer">
        <Upload className="w-12 h-12 text-blue-500 mb-2" />
        <span className="text-lg font-semibold text-gray-700">Upload CSV File</span>
        <span className="text-sm text-gray-500 mt-1">Drag and drop or click to select</span>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
        />
      </label>
    </div>
  );
};

export default FileUpload;