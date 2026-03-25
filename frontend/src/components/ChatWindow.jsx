import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../services/api";
import MessageBubble from "./MessageBubble";
import ListingCard from "./ListingCard";
import InputBar from "./InputBar";
import StarterPrompts from "./StarterPrompts";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text) => {
    if (!text.trim() || loading) return;

    const userMsg = { role: "user", content: text };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const { data } = await sendMessage(text);
      setMessages(prev => [...prev, { role: "assistant", content: data.reply }]);
      setListings(data.listings || []);
    } catch {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, something went wrong. Please try again."
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4 shadow-sm">
        <h1 className="text-xl font-bold text-gray-900">🏠 BLR Rentals</h1>
        <p className="text-sm text-gray-500">AI-powered Bangalore rental finder</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && (
          <StarterPrompts onSelect={handleSend} />
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && (
          <div className="flex gap-2 items-center text-gray-400 px-4">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Listing Cards */}
      {listings.length > 0 && (
        <div className="border-t bg-white px-4 py-4">
          <p className="text-xs text-gray-500 mb-3 font-medium uppercase tracking-wide">
            Relevant Listings
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-64 overflow-y-auto">
            {listings.map(l => <ListingCard key={l.id} listing={l} />)}
          </div>
        </div>
      )}

      <InputBar onSend={handleSend} loading={loading} />
    </div>
  );
}