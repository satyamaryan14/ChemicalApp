import React from 'react';

const HistoryTable = ({ history }) => {
  return (
    <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '20px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
      <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>Recent Upload History</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #f0f0f0', textAlign: 'left' }}>
            <th style={{ padding: '10px', color: '#666' }}>Filename</th>
            <th style={{ padding: '10px', color: '#666' }}>Date Uploaded</th>
            <th style={{ padding: '10px', color: '#666' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #f9f9f9' }}>
              <td style={{ padding: '12px', fontWeight: '500' }}>{item.filename}</td>
              <td style={{ padding: '12px', color: '#666' }}>{item.uploaded_at?.slice(0, 10)}</td>
              <td style={{ padding: '12px' }}>
                <span style={{
                  backgroundColor: '#e6f4ea',
                  color: '#1e7e34',
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '12px',
                  fontWeight: 'bold'
                }}>Processed</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryTable;