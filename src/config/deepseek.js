// DeepSeek API 配置
export const DEEPSEEK_CONFIG = {
  // DeepSeek API 端点
  API_URL: 'https://api.deepseek.com/v1/chat/completions',
  
  // API 密钥 (实际使用时从环境变量获取)
  API_KEY: process.env.REACT_APP_DEEPSEEK_API_KEY || 'your-deepseek-api-key-here',
  
  // 模型配置
  MODEL: 'deepseek-chat',
  
  // 请求配置
  REQUEST_CONFIG: {
    temperature: 0.7,
    max_tokens: 1000,
    top_p: 0.9,
    frequency_penalty: 0,
    presence_penalty: 0
  }
};

// 系统提示词
export const SYSTEM_PROMPT = `你是Multi-Agent DSL Platform的专业AI助手。你的任务是帮助用户解决关于多智能体系统、DSL原语、智能体协作等问题。

平台功能包括：
1. 多智能体协作：城市管理、交通管理、天气监测、停车管理等
2. DSL原语：EVENT_ROUTE、LLM_DRIVE、SYSTEM_SCHEDULE、AGENT_COLLABORATE、CACHE_OPTIMIZE
3. 实时监控：系统状态、性能指标、任务执行
4. 企业级功能：用户管理、通知中心、设置面板

请用专业、友好的语气回答用户问题，提供准确的技术指导。如果用户询问的问题不在平台功能范围内，请礼貌地引导用户到相关功能或建议联系技术支持。`;

// DeepSeek API 调用函数
export const callDeepSeekAPI = async (userMessage, conversationHistory = []) => {
  try {
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...conversationHistory,
      { role: 'user', content: userMessage }
    ];

    const response = await fetch(DEEPSEEK_CONFIG.API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DEEPSEEK_CONFIG.API_KEY}`
      },
      body: JSON.stringify({
        model: DEEPSEEK_CONFIG.MODEL,
        messages: messages,
        ...DEEPSEEK_CONFIG.REQUEST_CONFIG
      })
    });

    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data.choices && data.choices.length > 0) {
      return data.choices[0].message.content;
    } else {
      throw new Error('API响应格式错误');
    }
    
  } catch (error) {
    console.error('DeepSeek API调用失败:', error);
    throw error;
  }
};

// 模拟API调用（用于演示）
export const callDeepSeekAPIMock = async (userMessage) => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
  
  // 根据用户消息内容提供相关响应
  const responses = {
    'dsl': "DSL原语是系统的核心组件。EVENT_ROUTE用于事件路由，LLM_DRIVE用于AI驱动决策，SYSTEM_SCHEDULE用于任务调度，AGENT_COLLABORATE用于智能体协作，CACHE_OPTIMIZE用于缓存优化。",
    '智能体': "多智能体协作需要确保所有智能体都处于活跃状态。您可以查看系统状态栏中的指标来监控智能体状态，包括CPU使用率、内存使用率等。",
    '性能': "如果遇到性能问题，建议检查CACHE_OPTIMIZE原语的配置，它可以优化数据缓存和共享效率。同时监控系统指标，确保资源使用合理。",
    '错误': "遇到错误时，请检查智能体配置、DSL原语使用是否正确。可以查看执行报告面板获取详细的错误信息和解决建议。",
    '默认': "根据您的问题，我建议您检查智能体的配置和DSL原语的使用。EVENT_ROUTE原语用于事件路由，SYSTEM_SCHEDULE用于任务调度。如果问题持续存在，请联系技术支持团队。"
  };
  
  // 根据关键词匹配响应
  const lowerMessage = userMessage.toLowerCase();
  for (const [keyword, response] of Object.entries(responses)) {
    if (lowerMessage.includes(keyword)) {
      return response;
    }
  }
  
  return responses['默认'];
};
