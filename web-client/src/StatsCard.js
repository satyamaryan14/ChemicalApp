import React from 'react';

const StatsCard = ({ title, value, unit, color, icon }) => {
  return (
    <div style={{
      backgroundColor: 'white',
      borderRadius: '12px',
      padding: '20px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      minWidth: '200px',
      borderLeft: `5px solid ${color}`
    }}>
      <div>
        <p style={{ color: '#888', margin: '0 0 5px 0', fontSize: '14px', fontWeight: '600' }}>
          {title.toUpperCase()}
        </p>
        <h2 style={{ margin: 0, fontSize: '28px', color: '#333' }}>
          {value} <span style={{ fontSize: '16px', color: '#999' }}>{unit}</span>
        </h2>
      </div>
      <div style={{ fontSize: '30px', opacity: 0.8 }}>
        {icon}
      </div>
    </div>
  );
};

export default StatsCard;