import React, { useState } from 'react';

export default function Communication() {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'John Smith (Landlord)', message: 'Hi, the maintenance crew will arrive tomorrow at 2 PM', timestamp: '2026-02-18 10:30', type: 'received' },
    { id: 2, sender: 'You', message: 'Thanks! I will be home', timestamp: '2026-02-18 10:35', type: 'sent' },
    { id: 3, sender: 'John Smith (Landlord)', message: 'Great, see you then!', timestamp: '2026-02-18 10:36', type: 'received' },
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedUser, setSelectedUser] = useState('John Smith (Landlord)');

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      setMessages([...messages, {
        id: Date.now(),
        sender: 'You',
        message: newMessage,
        timestamp: new Date().toLocaleString(),
        type: 'sent'
      }]);
      setNewMessage('');
    }
  };

  const conversations = [
    'John Smith (Landlord)',
    'Maintenance Team',
    'Property Manager'
  ];

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif', display: 'flex', gap: 20, height: 'calc(100vh - 100px)' }}>
      <div style={{ width: '25%', border: '1px solid #ddd', borderRadius: 8, padding: 12, overflowY: 'auto' }}>
        <h3>Conversations</h3>
        {conversations.map(conv => (
          <div
            key={conv}
            onClick={() => setSelectedUser(conv)}
            style={{
              padding: 12,
              marginBottom: 8,
              backgroundColor: selectedUser === conv ? '#007bff' : '#f0f0f0',
              color: selectedUser === conv ? 'white' : 'black',
              borderRadius: 4,
              cursor: 'pointer'
            }}
          >
            {conv}
          </div>
        ))}
      </div>
      <div style={{ flex: 1, border: '1px solid #ddd', borderRadius: 8, display: 'flex', flexDirection: 'column' }}>
        <div style={{ borderBottom: '1px solid #ddd', padding: 16 }}>
          <h3 style={{ margin: 0 }}>{selectedUser}</h3>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: 16 }}>
          {messages.map(msg => (
            <div key={msg.id} style={{
              marginBottom: 16,
              textAlign: msg.type === 'sent' ? 'right' : 'left'
            }}>
              <div style={{
                display: 'inline-block',
                backgroundColor: msg.type === 'sent' ? '#007bff' : '#e0e0e0',
                color: msg.type === 'sent' ? 'white' : 'black',
                padding: 12,
                borderRadius: 8,
                maxWidth: '70%'
              }}>
                <p style={{ margin: '0 0 4px 0' }}>{msg.message}</p>
                <p style={{ margin: 0, fontSize: 12, opacity: 0.7 }}>{msg.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
        <div style={{ borderTop: '1px solid #ddd', padding: 16, display: 'flex', gap: 8 }}>
          <input
            type="text"
            placeholder="Type your message..."
            value={newMessage}
            onChange={e => setNewMessage(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
            style={{ flex: 1, fontSize: 14, padding: 8, borderRadius: 4, border: '1px solid #ddd' }}
          />
          <button onClick={handleSendMessage} style={{ fontSize: 16, padding: 8, backgroundColor: '#007bff', color: 'white', cursor: 'pointer', borderRadius: 4 }}>Send</button>
        </div>
      </div>
    </div>
  );
}