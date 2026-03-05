import React, { useState, useRef, useEffect } from 'react';
import { aiAgentsAPI } from '../../services/aiAgents';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export default function CustomerCareAI() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const userId = 'demo_user'; // In real app, get from auth context

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await aiAgentsAPI.customerCare(userId, inputMessage, sessionId);
      const data = response.data;

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
      setSessionId(data.session_id);

      // Show actions taken if any
      if (data.actions_taken && data.actions_taken.length > 0) {
        const actionMessage: Message = {
          id: (Date.now() + 2).toString(),
          text: `Actions taken: ${data.actions_taken.map((a: any) => a.action).join(', ')}`,
          sender: 'ai',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, actionMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const startNewConversation = () => {
    setMessages([]);
    setSessionId(undefined);
  };

  return (
    <div className="max-w-4xl mx-auto p-4 h-screen flex flex-col">
      <div className="bg-white rounded-lg shadow-lg flex flex-col h-full">
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
          <h1 className="text-xl font-bold">FIND AI Customer Care</h1>
          <button
            onClick={startNewConversation}
            className="bg-blue-700 hover:bg-blue-800 px-3 py-1 rounded text-sm"
          >
            New Conversation
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <p className="text-lg mb-2">👋 Welcome to FIND AI Customer Care!</p>
              <p>How can I help you with your rental needs today?</p>
              <div className="mt-4 space-y-2">
                <p className="text-sm">Try asking:</p>
                <div className="space-y-1 text-xs text-gray-400">
                  <p>• "When is my rent due?"</p>
                  <p>• "Find me a 2-bedroom in Westlands"</p>
                  <p>• "Pay my rent"</p>
                  <p>• "Report maintenance issue"</p>
                </div>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.text}</p>
                <p className={`text-xs mt-1 ${
                  message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                }`}>
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                  <span>AI is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSendMessage} className="p-4 border-t">
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !inputMessage.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}