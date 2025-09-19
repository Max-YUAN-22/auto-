#!/usr/bin/env node

// WebSocket连接测试脚本
const io = require('socket.io-client');

console.log('🔌 测试WebSocket连接...');

const socket = io('http://localhost:8008', {
  transports: ['websocket', 'polling'],
  timeout: 10000,
  forceNew: true
});

socket.on('connect', () => {
  console.log('✅ WebSocket连接成功!');
  console.log('📡 Socket ID:', socket.id);
  
  // 发送测试消息
  socket.emit('message', {
    type: 'test',
    data: { message: 'Hello from test script' }
  });
});

socket.on('connection_successful', (data) => {
  console.log('🎉 收到连接确认:', data);
});

socket.on('disconnect', (reason) => {
  console.log('❌ WebSocket断开连接:', reason);
});

socket.on('connect_error', (error) => {
  console.log('❌ WebSocket连接错误:', error.message);
});

socket.on('message', (data) => {
  console.log('📨 收到消息:', data);
});

// 5秒后关闭连接
setTimeout(() => {
  console.log('🔄 关闭测试连接');
  socket.disconnect();
  process.exit(0);
}, 5000);