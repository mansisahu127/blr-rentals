import { useState } from "react";
import { Send } from "lucide-react";

export default function InputBar({ onSend, loading }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim() || loading) return;
    onSend(text.trim());
    setText("");
  };

  const handleKeyDown = (e) => {
    // Send on Enter, new line on Shift+Enter
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t bg-white px-4 py-3">
      <div className="flex items-end gap-2 max-w-4xl mx-auto">
        
        {/* Text Input */}
        <textarea
          rows={1}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about rentals in Bangalore..."
          disabled={loading}
          className="flex-1 resize-none rounded-2xl border border-gray-200 
                     bg-gray-50 px-4 py-3 text-sm text-gray-800
                     placeholder:text-gray-400 focus:outline-none 
                     focus:ring-2 focus:ring-emerald-400 focus:border-transparent
                     disabled:opacity-50 disabled:cursor-not-allowed
                     max-h-32 overflow-y-auto"
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={!text.trim() || loading}
          className="w-11 h-11 rounded-full bg-emerald-500 flex items-center 
                     justify-center text-white shrink-0
                     hover:bg-emerald-600 transition-colors
                     disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading
            ? <div className="w-4 h-4 border-2 border-white border-t-transparent 
                              rounded-full animate-spin" />
            : <Send size={16} />
          }
        </button>

      </div>

      {/* Hint text */}
      <p className="text-center text-xs text-gray-400 mt-2">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  );
}