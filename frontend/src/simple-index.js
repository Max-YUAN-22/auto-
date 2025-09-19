import React from 'react';
import ReactDOM from 'react-dom/client';

// 简单的测试组件
function SimpleApp() {
  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif',
      background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
      color: 'white',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <h1>🚀 多智能体DSL框架</h1>
      <p>企业级多智能体DSL框架 - 自适应调度与协作学习的创新解决方案</p>
      
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '20px',
        borderRadius: '10px',
        margin: '20px 0',
        textAlign: 'center'
      }}>
        <h2>✅ 部署成功！</h2>
        <p>React应用正在正常运行</p>
        <p>时间: {new Date().toLocaleString('zh-CN')}</p>
      </div>
      
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '20px',
        borderRadius: '10px',
        margin: '20px 0'
      }}>
        <h3>🔧 功能测试</h3>
        <button 
          onClick={() => alert('JavaScript功能正常！')}
          style={{
            background: '#4CAF50',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: 'pointer',
            margin: '5px'
          }}
        >
          测试JavaScript
        </button>
        <button 
          onClick={() => {
            const info = {
              userAgent: navigator.userAgent,
              screen: `${screen.width}x${screen.height}`,
              viewport: `${window.innerWidth}x${window.innerHeight}`,
              language: navigator.language,
              url: window.location.href
            };
            alert(`系统信息:\n${JSON.stringify(info, null, 2)}`);
          }}
          style={{
            background: '#2196F3',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: 'pointer',
            margin: '5px'
          }}
        >
          系统信息
        </button>
      </div>
      
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        padding: '20px',
        borderRadius: '10px',
        margin: '20px 0'
      }}>
        <h3>🌐 访问地址</h3>
        <p><strong>Vercel:</strong> https://multi-agent-ds-lframework-2025.vercel.app</p>
        <p><strong>GitHub Pages:</strong> https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/</p>
      </div>
    </div>
  );
}

// 渲染应用
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <SimpleApp />
  </React.StrictMode>
);
