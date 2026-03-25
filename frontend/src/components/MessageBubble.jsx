export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex items-end gap-2 ${isUser ? "justify-end" : "justify-start"}`}>
      
      {/* AI Avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center 
                        justify-center text-white text-sm font-bold shrink-0">
          AI
        </div>
      )}

      {/* Bubble */}
      <div
        className={`
          max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed
          ${isUser
            ? "bg-emerald-500 text-white rounded-br-none"
            : "bg-white text-gray-800 rounded-bl-none shadow-sm border border-gray-100"
          }
        `}
      >
        {message.content}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center 
                        justify-center text-gray-600 text-sm font-bold shrink-0">
          U
        </div>
      )}

    </div>
  );
}