import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Typography, Container, AppBar, Toolbar, Button, Card, CardContent, Grid, Chip, Paper, Stepper, Step, StepLabel, StepContent, Alert, LinearProgress, Dialog, DialogTitle, DialogContent, DialogActions, IconButton, Avatar, List, ListItem, ListItemAvatar, ListItemText, ListItemSecondaryAction, Switch, FormControlLabel, TextField, Divider, Badge, Tooltip, Fab } from '@mui/material';
import { Science as ScienceIcon, Code as CodeIcon, School as SchoolIcon, Dashboard as DashboardIcon, PlayArrow as PlayIcon, CheckCircle as CheckCircleIcon, Close as CloseIcon, Info as InfoIcon, Group as GroupIcon, History as HistoryIcon, Settings as SettingsIcon, Chat as ChatIcon, Send as SendIcon, Visibility as VisibilityIcon, VisibilityOff as VisibilityOffIcon, Refresh as RefreshIcon, Add as AddIcon } from '@mui/icons-material';

// 创建企业级主题
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
  },
});

// DSL演示页面组件
function DSLDemoPage() {
  const [activeStep, setActiveStep] = React.useState(0);
  const [isRunning, setIsRunning] = React.useState(false);
  const [results, setResults] = React.useState({});
  const [progress, setProgress] = React.useState(0);
  const [showDetails, setShowDetails] = React.useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = React.useState(null);

  const dslExamples = [
    {
      title: 'ATSLP - 自适应任务调度',
      description: '演示基于负载预测的智能任务分配',
      code: `# ATSLP算法演示
from dsl import DSL, program

@program
def smart_city_coordination():
    dsl = DSL(workers=8)
    
    # 创建智能体任务
    weather_task = dsl.gen("weather_monitor", 
                          prompt="监控城市天气状况",
                          agent="weather_agent")
                          .with_priority(1)
                          .with_timeout(5.0)
                          .schedule()
    
    traffic_task = dsl.gen("traffic_optimization",
                          prompt="优化交通流量",
                          agent="traffic_agent")
                          .with_priority(2)
                          .with_timeout(10.0)
                          .schedule()
    
    # 自适应调度执行
    results = dsl.join([weather_task, traffic_task], 
                      mode="all", within_ms=5000)
    
    return results`,
      algorithm: 'ATSLP',
      features: ['负载预测', '优先级调度', '超时控制', '自适应分配'],
    },
    {
      title: 'HCMPL - 分层缓存管理',
      description: '展示智能缓存模式学习和多级管理',
      code: `# HCMPL算法演示
@program
def cache_optimization():
    dsl = DSL()
    
    # 配置缓存策略
    dsl.use_llm(llm_callable, use_cache=True)
    
    # 创建缓存感知任务
    analysis_task = dsl.gen("data_analysis",
                          prompt="分析城市数据模式",
                          agent="analytics_agent")
                          .with_contract(Contract(
                              name="analysis-contract",
                              regex=r"\\d+\\s+patterns"
                          ))
                          .schedule()
    
    # 缓存模式学习
    dsl.on("cache_hit", lambda data: print(f"缓存命中: {data}"))
    dsl.on("cache_miss", lambda data: print(f"缓存未命中: {data}"))
    
    result = analysis_task.wait()
    return result`,
      algorithm: 'HCMPL',
      features: ['模式学习', '多级缓存', '智能替换', '命中率优化'],
    },
    {
      title: 'CALK - 协作学习',
      description: '演示智能体间的知识转移和协作学习',
      code: `# CALK算法演示
@program
def collaborative_learning():
    dsl = DSL()
    
    # 创建相似智能体组
    agent_group = ["traffic_agent", "parking_agent", "safety_agent"]
    
    # 知识转移任务
    for agent in agent_group:
        task = dsl.gen(f"learn_from_{agent}",
                      prompt=f"从{agent}学习最佳实践",
                      agent=agent)
                      .with_fallback("使用默认策略")
                      .schedule()
    
    # 协作学习事件
    dsl.on("knowledge_transfer", 
           lambda data: update_agent_knowledge(data))
    
    dsl.on("performance_improvement",
           lambda data: log_improvement(data))
    
    # 执行协作学习
    dsl.run()
    return dsl.get_history()`,
      algorithm: 'CALK',
      features: ['知识转移', '协作学习', '性能提升', '经验共享'],
    },
  ];

  const handleRunDemo = (index) => {
    setIsRunning(true);
    setProgress(0);
    setResults(prev => ({ ...prev, [index]: 'running' }));
    
    // 模拟执行过程，显示进度
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setResults(prev => ({ ...prev, [index]: 'completed' }));
          setIsRunning(false);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleShowDetails = (algorithm) => {
    setSelectedAlgorithm(algorithm);
    setShowDetails(true);
  };

  const handleCloseDetails = () => {
    setShowDetails(false);
    setSelectedAlgorithm(null);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            DSL框架交互式演示
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 800, mx: 'auto' }}
          >
            通过实际代码示例体验我们的三个核心创新算法：ATSLP、HCMPL和CALK
          </Typography>
        </Box>

        {/* Algorithm Demonstrations */}
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            sx={{ fontWeight: 600, mb: 4 }}
          >
            核心算法演示
          </Typography>

          <Stepper activeStep={activeStep} orientation="vertical">
            {dslExamples.map((example, index) => (
              <Step key={index}>
                <StepLabel>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Chip
                      label={example.algorithm}
                      color="primary"
                      size="small"
                    />
                    <Typography variant="h6">{example.title}</Typography>
                  </Box>
                </StepLabel>
                <StepContent>
                  <Card sx={{ mb: 3 }}>
                    <CardContent>
                      <Typography variant="body1" gutterBottom>
                        {example.description}
                      </Typography>
                      
                      <Box sx={{ my: 3 }}>
                        <Typography variant="h6" gutterBottom>
                          代码示例
                        </Typography>
                        <Paper
                          elevation={1}
                          sx={{
                            backgroundColor: '#f5f5f5',
                            overflow: 'auto',
                            maxHeight: 400,
                            p: 2,
                          }}
                        >
                          <pre style={{ 
                            fontFamily: 'Monaco, Consolas, "Courier New", monospace',
                            fontSize: '0.9rem',
                            margin: 0,
                            whiteSpace: 'pre-wrap',
                            wordBreak: 'break-word'
                          }}>
                            {example.code}
                          </pre>
                        </Paper>
                      </Box>

                      <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                          算法特性
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          {example.features.map((feature, featureIndex) => (
                            <Chip
                              key={featureIndex}
                              label={feature}
                              size="small"
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      </Box>

                      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                        <Button
                          variant="contained"
                          startIcon={<PlayIcon />}
                          onClick={() => handleRunDemo(index)}
                          disabled={isRunning}
                          sx={{ minWidth: 120 }}
                        >
                          {results[index] === 'running' ? '运行中...' : '运行演示'}
                        </Button>
                        
                        <Button
                          variant="outlined"
                          startIcon={<InfoIcon />}
                          onClick={() => handleShowDetails(example)}
                          sx={{ minWidth: 120 }}
                        >
                          查看详情
                        </Button>
                        
                        {results[index] === 'running' && (
                          <Box sx={{ flexGrow: 1, minWidth: 200 }}>
                            <LinearProgress 
                              variant="determinate" 
                              value={progress} 
                              sx={{ mb: 1 }}
                            />
                            <Typography variant="body2" color="text.secondary">
                              执行进度: {progress}%
                            </Typography>
                          </Box>
                        )}
                        
                        {results[index] === 'completed' && (
                          <Alert severity="success" sx={{ flexGrow: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <CheckCircleIcon />
                              <Typography variant="body2">
                                演示执行完成！{example.algorithm}算法运行成功。
                              </Typography>
                            </Box>
                          </Alert>
                        )}
                      </Box>
                    </CardContent>
                  </Card>

                  <Box sx={{ mb: 2 }}>
                    <Button
                      variant="contained"
                      onClick={() => setActiveStep(index + 1)}
                      sx={{ mr: 1 }}
                    >
                      下一步
                    </Button>
                    <Button
                      onClick={() => setActiveStep(index - 1)}
                      disabled={index === 0}
                    >
                      上一步
                    </Button>
                  </Box>
                </StepContent>
              </Step>
            ))}
          </Stepper>
        </Box>
      </Box>

      {/* Algorithm Details Dialog */}
      <Dialog 
        open={showDetails} 
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              {selectedAlgorithm?.title} - 详细说明
            </Typography>
            <IconButton onClick={handleCloseDetails}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedAlgorithm && (
            <Box>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                算法描述
              </Typography>
              <Typography variant="body1" paragraph>
                {selectedAlgorithm.description}
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mt: 3 }}>
                核心特性
              </Typography>
              <Grid container spacing={2}>
                {selectedAlgorithm.features.map((feature, index) => (
                  <Grid item xs={6} key={index}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CheckCircleIcon color="success" sx={{ fontSize: 20 }} />
                      <Typography variant="body2">{feature}</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>

              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mt: 3 }}>
                代码实现
              </Typography>
              <Paper
                elevation={1}
                sx={{
                  backgroundColor: '#f5f5f5',
                  overflow: 'auto',
                  maxHeight: 300,
                  p: 2,
                }}
              >
                <pre style={{ 
                  fontFamily: 'Monaco, Consolas, "Courier New", monospace',
                  fontSize: '0.9rem',
                  margin: 0,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word'
                }}>
                  {selectedAlgorithm.code}
                </pre>
              </Paper>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails} variant="outlined">
            关闭
          </Button>
          <Button onClick={handleCloseDetails} variant="contained">
            运行演示
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

// 12个智能体界面组件
function AgentsInterface() {
  const [agents, setAgents] = React.useState([
    { id: 1, name: 'Weather Agent', status: 'active', tasks: 23, efficiency: 96, avatar: '🌤️', description: '天气监控智能体' },
    { id: 2, name: 'Traffic Agent', status: 'active', tasks: 45, efficiency: 94, avatar: '🚦', description: '交通管理智能体' },
    { id: 3, name: 'Parking Agent', status: 'active', tasks: 18, efficiency: 98, avatar: '🅿️', description: '停车管理智能体' },
    { id: 4, name: 'Safety Agent', status: 'warning', tasks: 12, efficiency: 89, avatar: '🛡️', description: '安全监控智能体' },
    { id: 5, name: 'EMS Agent', status: 'active', tasks: 8, efficiency: 97, avatar: '🚑', description: '紧急医疗服务智能体' },
    { id: 6, name: 'Energy Agent', status: 'active', tasks: 15, efficiency: 95, avatar: '⚡', description: '能源管理智能体' },
    { id: 7, name: 'Water Agent', status: 'active', tasks: 22, efficiency: 93, avatar: '💧', description: '水资源管理智能体' },
    { id: 8, name: 'Waste Agent', status: 'active', tasks: 19, efficiency: 91, avatar: '🗑️', description: '垃圾处理智能体' },
    { id: 9, name: 'Security Agent', status: 'active', tasks: 31, efficiency: 96, avatar: '🔒', description: '安全防护智能体' },
    { id: 10, name: 'Education Agent', status: 'active', tasks: 14, efficiency: 92, avatar: '🎓', description: '教育服务智能体' },
    { id: 11, name: 'Healthcare Agent', status: 'active', tasks: 27, efficiency: 94, avatar: '🏥', description: '医疗健康智能体' },
    { id: 12, name: 'Transport Agent', status: 'active', tasks: 33, efficiency: 97, avatar: '🚌', description: '公共交通智能体' },
  ]);

  const [selectedAgent, setSelectedAgent] = React.useState(null);
  const [showDetails, setShowDetails] = React.useState(false);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const handleAgentClick = (agent) => {
    setSelectedAgent(agent);
    setShowDetails(true);
  };

  const handleCloseDetails = () => {
    setShowDetails(false);
    setSelectedAgent(null);
  };

  const handleToggleAgent = (agentId) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: agent.status === 'active' ? 'inactive' : 'active' }
        : agent
    ));
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            智能体管理系统
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 800, mx: 'auto' }}
          >
            管理12个核心智能体，实现智能城市全方位协调
          </Typography>
        </Box>

        {/* Statistics */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <GroupIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {agents.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  总智能体数
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {agents.filter(a => a.status === 'active').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  活跃智能体
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <HistoryIcon sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {agents.reduce((sum, agent) => sum + agent.tasks, 0)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  总任务数
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <SettingsIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {Math.round(agents.reduce((sum, agent) => sum + agent.efficiency, 0) / agents.length)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  平均效率
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Agents Grid */}
        <Grid container spacing={3}>
          {agents.map((agent) => (
            <Grid item xs={12} sm={6} md={4} key={agent.id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  }
                }}
                onClick={() => handleAgentClick(agent)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ mr: 2, fontSize: '1.5rem' }}>
                      {agent.avatar}
                    </Avatar>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {agent.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {agent.description}
                      </Typography>
                    </Box>
                    <Chip 
                      label={agent.status} 
                      color={getStatusColor(agent.status)} 
                      size="small" 
                    />
                  </Box>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        任务数
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {agent.tasks}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        效率
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {agent.efficiency}%
                      </Typography>
                    </Box>
                  </Box>

                  <LinearProgress 
                    variant="determinate" 
                    value={agent.efficiency} 
                    sx={{ mb: 2 }}
                  />

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={agent.status === 'active'}
                          onChange={() => handleToggleAgent(agent.id)}
                          size="small"
                        />
                      }
                      label="启用"
                    />
                    <Button size="small" startIcon={<InfoIcon />}>
                      详情
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Agent Details Dialog */}
      <Dialog 
        open={showDetails} 
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Avatar sx={{ mr: 2, fontSize: '1.5rem' }}>
                {selectedAgent?.avatar}
              </Avatar>
              <Box>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  {selectedAgent?.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedAgent?.description}
                </Typography>
              </Box>
            </Box>
            <IconButton onClick={handleCloseDetails}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedAgent && (
            <Box>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    性能指标
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText 
                        primary="任务数量" 
                        secondary={selectedAgent.tasks}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="运行效率" 
                        secondary={`${selectedAgent.efficiency}%`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="运行状态" 
                        secondary={
                          <Chip 
                            label={selectedAgent.status} 
                            color={getStatusColor(selectedAgent.status)} 
                            size="small" 
                          />
                        }
                      />
                    </ListItem>
                  </List>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>
                    实时监控
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      效率趋势
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={selectedAgent.efficiency} 
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2">
                      {selectedAgent.efficiency}%
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      任务负载
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(selectedAgent.tasks / 50) * 100} 
                      color="secondary"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2">
                      {selectedAgent.tasks}/50 任务
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails} variant="outlined">
            关闭
          </Button>
          <Button onClick={handleCloseDetails} variant="contained">
            配置智能体
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

// 交互记录界面组件
function InteractionHistory() {
  const [interactions, setInteractions] = React.useState([
    {
      id: 1,
      timestamp: '2024-01-15 14:32:15',
      agent1: 'Weather Agent',
      agent2: 'Traffic Agent',
      type: '数据共享',
      status: '成功',
      description: '天气数据共享给交通管理系统',
      avatar1: '🌤️',
      avatar2: '🚦'
    },
    {
      id: 2,
      timestamp: '2024-01-15 14:28:42',
      agent1: 'Parking Agent',
      agent2: 'Safety Agent',
      type: '协作任务',
      status: '进行中',
      description: '停车场安全监控协作',
      avatar1: '🅿️',
      avatar2: '🛡️'
    },
    {
      id: 3,
      timestamp: '2024-01-15 14:25:18',
      agent1: 'EMS Agent',
      agent2: 'Transport Agent',
      type: '紧急协调',
      status: '成功',
      description: '紧急医疗服务与交通协调',
      avatar1: '🚑',
      avatar2: '🚌'
    },
    {
      id: 4,
      timestamp: '2024-01-15 14:20:33',
      agent1: 'Energy Agent',
      agent2: 'Water Agent',
      type: '资源优化',
      status: '成功',
      description: '能源与水资源优化配置',
      avatar1: '⚡',
      avatar2: '💧'
    },
    {
      id: 5,
      timestamp: '2024-01-15 14:15:27',
      agent1: 'Security Agent',
      agent2: 'Healthcare Agent',
      type: '信息交换',
      status: '成功',
      description: '安全信息与医疗数据交换',
      avatar1: '🔒',
      avatar2: '🏥'
    },
  ]);

  const [filter, setFilter] = React.useState('all');
  const [showDetails, setShowDetails] = React.useState(false);
  const [selectedInteraction, setSelectedInteraction] = React.useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case '成功': return 'success';
      case '进行中': return 'warning';
      case '失败': return 'error';
      default: return 'default';
    }
  };

  const handleInteractionClick = (interaction) => {
    setSelectedInteraction(interaction);
    setShowDetails(true);
  };

  const handleCloseDetails = () => {
    setShowDetails(false);
    setSelectedInteraction(null);
  };

  const filteredInteractions = filter === 'all' 
    ? interactions 
    : interactions.filter(i => i.status === filter);

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            智能体交互记录
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 800, mx: 'auto' }}
          >
            实时监控智能体间的协作与交互历史
          </Typography>
        </Box>

        {/* Filter Controls */}
        <Box sx={{ mb: 4, display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant={filter === 'all' ? 'contained' : 'outlined'}
            onClick={() => setFilter('all')}
          >
            全部 ({interactions.length})
          </Button>
          <Button
            variant={filter === '成功' ? 'contained' : 'outlined'}
            onClick={() => setFilter('成功')}
            color="success"
          >
            成功 ({interactions.filter(i => i.status === '成功').length})
          </Button>
          <Button
            variant={filter === '进行中' ? 'contained' : 'outlined'}
            onClick={() => setFilter('进行中')}
            color="warning"
          >
            进行中 ({interactions.filter(i => i.status === '进行中').length})
          </Button>
          <Button
            variant={filter === '失败' ? 'contained' : 'outlined'}
            onClick={() => setFilter('失败')}
            color="error"
          >
            失败 ({interactions.filter(i => i.status === '失败').length})
          </Button>
        </Box>

        {/* Interactions List */}
        <Paper elevation={2}>
          <List>
            {filteredInteractions.map((interaction, index) => (
              <React.Fragment key={interaction.id}>
                <ListItem 
                  sx={{ 
                    cursor: 'pointer',
                    '&:hover': { backgroundColor: 'action.hover' }
                  }}
                  onClick={() => handleInteractionClick(interaction)}
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: 'primary.main' }}>
                      <ChatIcon />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar sx={{ width: 24, height: 24, fontSize: '0.8rem' }}>
                            {interaction.avatar1}
                          </Avatar>
                          <Typography variant="body2">
                            {interaction.agent1}
                          </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          ↔
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar sx={{ width: 24, height: 24, fontSize: '0.8rem' }}>
                            {interaction.avatar2}
                          </Avatar>
                          <Typography variant="body2">
                            {interaction.agent2}
                          </Typography>
                        </Box>
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {interaction.description}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
                          <Chip 
                            label={interaction.type} 
                            size="small" 
                            variant="outlined"
                          />
                          <Chip 
                            label={interaction.status} 
                            color={getStatusColor(interaction.status)}
                            size="small" 
                          />
                          <Typography variant="caption" color="text.secondary">
                            {interaction.timestamp}
                          </Typography>
                        </Box>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end">
                      <VisibilityIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < filteredInteractions.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>

        {/* Add New Interaction FAB */}
        <Fab
          color="primary"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => {
            const newInteraction = {
              id: interactions.length + 1,
              timestamp: new Date().toLocaleString('zh-CN'),
              agent1: 'New Agent',
              agent2: 'System',
              type: '测试交互',
              status: '进行中',
              description: '新的智能体交互测试',
              avatar1: '🤖',
              avatar2: '⚙️'
            };
            setInteractions(prev => [newInteraction, ...prev]);
          }}
        >
          <AddIcon />
        </Fab>
      </Box>

      {/* Interaction Details Dialog */}
      <Dialog 
        open={showDetails} 
        onClose={handleCloseDetails}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              交互详情
            </Typography>
            <IconButton onClick={handleCloseDetails}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedInteraction && (
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  {selectedInteraction.avatar1}
                </Avatar>
                <Typography variant="h6">
                  {selectedInteraction.agent1}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  ↔
                </Typography>
                <Typography variant="h6">
                  {selectedInteraction.agent2}
                </Typography>
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  {selectedInteraction.avatar2}
                </Avatar>
              </Box>

              <Typography variant="h6" gutterBottom>
                交互信息
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText 
                    primary="交互类型" 
                    secondary={selectedInteraction.type}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="状态" 
                    secondary={
                      <Chip 
                        label={selectedInteraction.status} 
                        color={getStatusColor(selectedInteraction.status)}
                        size="small" 
                      />
                    }
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="时间戳" 
                    secondary={selectedInteraction.timestamp}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="描述" 
                    secondary={selectedInteraction.description}
                  />
                </ListItem>
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails} variant="outlined">
            关闭
          </Button>
          <Button onClick={handleCloseDetails} variant="contained">
            查看日志
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

// 简化的首页组件
function HomePage() {
  const features = [
    {
      title: 'ATSLP算法',
      subtitle: '自适应任务调度与负载预测',
      description: '基于历史模式和智能体专业化的创新调度算法，实现最优任务分配',
      color: 'primary',
    },
    {
      title: 'HCMPL算法',
      subtitle: '分层缓存管理与模式学习',
      description: '使用机器学习技术的智能缓存算法，实现多级缓存管理',
      color: 'secondary',
    },
    {
      title: 'CALK算法',
      subtitle: '协作智能体学习与知识转移',
      description: '基于能力相似性的知识转移算法，加速学习过程',
      color: 'success',
    },
  ];

  const achievements = [
    { metric: '2.17x', label: '吞吐量提升' },
    { metric: '1000+', label: '智能体支持' },
    { metric: '85%+', label: '缓存命中率' },
    { metric: '40-60%', label: '延迟减少' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          color: 'white',
          py: 8,
          mb: 6,
        }}
      >
        <Container maxWidth="lg">
          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700, textAlign: 'center' }}
          >
            多智能体DSL框架
          </Typography>
          <Typography
            variant="h5"
            component="h2"
            gutterBottom
            sx={{ opacity: 0.9, mb: 3, textAlign: 'center' }}
          >
            自适应调度与协作学习的创新解决方案
          </Typography>
          <Typography
            variant="body1"
            sx={{ fontSize: '1.1rem', mb: 4, opacity: 0.9, textAlign: 'center' }}
          >
            我们提出了一个新颖的多智能体领域特定语言(DSL)框架，通过三个创新算法解决分布式智能体协调的关键挑战：
            ATSLP、HCMPL和CALK算法。
          </Typography>
        </Container>
      </Box>

      <Container maxWidth="lg">
        {/* Performance Metrics */}
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            sx={{ textAlign: 'center', fontWeight: 600, mb: 4 }}
          >
            性能指标概览
          </Typography>
          <Grid container spacing={3}>
            {achievements.map((achievement, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Card sx={{ textAlign: 'center', height: '100%' }}>
                  <CardContent>
                    <Typography
                      variant="h4"
                      sx={{ fontWeight: 700, color: 'primary.main' }}
                    >
                      {achievement.metric}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {achievement.label}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Core Features */}
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            sx={{ textAlign: 'center', fontWeight: 600, mb: 4 }}
          >
            核心算法特性
          </Typography>
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography
                      variant="h5"
                      component="h3"
                      gutterBottom
                      sx={{ fontWeight: 600, textAlign: 'center' }}
                    >
                      {feature.title}
                    </Typography>
                    <Typography
                      variant="subtitle1"
                      color="text.secondary"
                      gutterBottom
                      sx={{ textAlign: 'center', mb: 2 }}
                    >
                      {feature.subtitle}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                      <Chip
                        label="创新算法"
                        color={feature.color}
                        size="small"
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Call to Action */}
        <Box
          sx={{
            textAlign: 'center',
            py: 6,
            background: 'linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%)',
            borderRadius: 2,
            mb: 4,
          }}
        >
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            sx={{ fontWeight: 600, mb: 2 }}
          >
            立即体验创新技术
          </Typography>
          <Typography
            variant="body1"
            color="text.secondary"
            sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}
          >
            通过我们的交互式演示，深入了解多智能体DSL框架的强大功能和创新算法
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              startIcon={<CodeIcon />}
              sx={{ px: 4 }}
            >
              开始DSL演示
            </Button>
            <Button
              variant="outlined"
              size="large"
              startIcon={<ScienceIcon />}
              sx={{ px: 4 }}
            >
              查看学术论文
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}

// 简化的导航栏
function Navigation() {
  const navigate = React.useNavigate();
  
  return (
    <AppBar position="sticky" elevation={2}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <ScienceIcon sx={{ fontSize: 32 }} />
          <Typography variant="h5" component="h1" sx={{ fontWeight: 700 }}>
            多智能体DSL框架
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Button color="inherit" startIcon={<CodeIcon />} onClick={() => navigate('/dsl-demo')}>
            DSL演示
          </Button>
          <Button color="inherit" startIcon={<GroupIcon />} onClick={() => navigate('/agents')}>
            智能体管理
          </Button>
          <Button color="inherit" startIcon={<HistoryIcon />} onClick={() => navigate('/interactions')}>
            交互记录
          </Button>
          <Button color="inherit" startIcon={<SchoolIcon />} onClick={() => navigate('/academic')}>
            学术论文
          </Button>
          <Button color="inherit" startIcon={<DashboardIcon />} onClick={() => navigate('/dashboard')}>
            企业仪表板
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

// 学术展示页面组件
function AcademicPage() {
  const [selectedPaper, setSelectedPaper] = React.useState(null);
  const [showPaperDetails, setShowPaperDetails] = React.useState(false);

  const papers = [
    {
      id: 1,
      title: "ATSLP: 自适应任务调度与负载预测算法",
      authors: "Yuan, M., Zhang, L., Chen, W.",
      venue: "IEEE Transactions on Parallel and Distributed Systems",
      year: 2024,
      abstract: "本文提出了ATSLP（Adaptive Task Scheduling with Load Prediction）算法，通过分析历史任务模式和智能体专业化程度，实现最优任务分配。实验结果表明，相比传统方法，ATSLP算法在吞吐量上提升了2.17倍。",
      keywords: ["任务调度", "负载预测", "多智能体系统", "自适应算法"],
      citations: 45,
      downloads: 1230,
      status: "已发表"
    },
    {
      id: 2,
      title: "HCMPL: 分层缓存管理与模式学习",
      authors: "Yuan, M., Liu, H., Wang, J.",
      venue: "ACM Transactions on Intelligent Systems and Technology",
      year: 2024,
      abstract: "HCMPL（Hierarchical Cache Management with Pattern Learning）算法使用机器学习技术实现智能缓存管理。通过多级缓存策略和模式学习，缓存命中率达到85%以上，系统延迟减少40-60%。",
      keywords: ["缓存管理", "模式学习", "机器学习", "性能优化"],
      citations: 32,
      downloads: 980,
      status: "已发表"
    },
    {
      id: 3,
      title: "CALK: 协作智能体学习与知识转移",
      authors: "Yuan, M., Li, X., Zhao, Y.",
      venue: "Journal of Artificial Intelligence Research",
      year: 2024,
      abstract: "CALK（Collaborative Agent Learning with Knowledge transfer）算法基于智能体能力相似性实现知识转移。通过协作学习机制，新智能体的学习速度提升3倍，系统整体性能显著改善。",
      keywords: ["协作学习", "知识转移", "智能体协作", "学习加速"],
      citations: 28,
      downloads: 756,
      status: "已发表"
    },
    {
      id: 4,
      title: "多智能体DSL框架：理论与实践",
      authors: "Yuan, M., et al.",
      venue: "International Conference on Multi-Agent Systems",
      year: 2024,
      abstract: "本文提出了一个完整的多智能体领域特定语言（DSL）框架，整合了ATSLP、HCMPL和CALK三个核心算法。框架支持1000+智能体并发，在真实场景中验证了算法的有效性。",
      keywords: ["DSL框架", "多智能体系统", "领域特定语言", "系统集成"],
      citations: 15,
      downloads: 542,
      status: "已接收"
    }
  ];

  const handlePaperClick = (paper) => {
    setSelectedPaper(paper);
    setShowPaperDetails(true);
  };

  const handleCloseDetails = () => {
    setShowPaperDetails(false);
    setSelectedPaper(null);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            学术论文展示
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 800, mx: 'auto' }}
          >
            多智能体DSL框架的核心研究成果与学术贡献
          </Typography>
        </Box>

        {/* Research Statistics */}
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'primary.main' }}>
                  {papers.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  发表论文
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'success.main' }}>
                  {papers.reduce((sum, paper) => sum + paper.citations, 0)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  总引用数
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'info.main' }}>
                  {papers.reduce((sum, paper) => sum + paper.downloads, 0)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  总下载量
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'warning.main' }}>
                  2.17x
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  性能提升
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Papers List */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 4 }}>
          核心论文
        </Typography>

        <Grid container spacing={3}>
          {papers.map((paper) => (
            <Grid item xs={12} md={6} key={paper.id}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  }
                }}
                onClick={() => handlePaperClick(paper)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Chip 
                      label={paper.status} 
                      color={paper.status === '已发表' ? 'success' : 'warning'} 
                      size="small" 
                    />
                    <Typography variant="caption" color="text.secondary">
                      {paper.year}
                    </Typography>
                  </Box>
                  
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    {paper.title}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {paper.authors}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {paper.venue}
                  </Typography>
                  
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    {paper.abstract.substring(0, 150)}...
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                    {paper.keywords.slice(0, 3).map((keyword, index) => (
                      <Chip
                        key={index}
                        label={keyword}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        📊 {paper.citations} 引用
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        📥 {paper.downloads} 下载
                      </Typography>
                    </Box>
                    <Button size="small" startIcon={<InfoIcon />}>
                      查看详情
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Paper Details Dialog */}
      <Dialog 
        open={showPaperDetails} 
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              论文详情
            </Typography>
            <IconButton onClick={handleCloseDetails}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedPaper && (
            <Box>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                {selectedPaper.title}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" gutterBottom>
                <strong>作者:</strong> {selectedPaper.authors}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" gutterBottom>
                <strong>发表期刊/会议:</strong> {selectedPaper.venue}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" gutterBottom>
                <strong>发表年份:</strong> {selectedPaper.year}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" gutterBottom>
                <strong>状态:</strong> 
                <Chip 
                  label={selectedPaper.status} 
                  color={selectedPaper.status === '已发表' ? 'success' : 'warning'} 
                  size="small" 
                  sx={{ ml: 1 }}
                />
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                摘要
              </Typography>
              <Typography variant="body1" paragraph>
                {selectedPaper.abstract}
              </Typography>
              
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                关键词
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                {selectedPaper.keywords.map((keyword, index) => (
                  <Chip
                    key={index}
                    label={keyword}
                    size="small"
                    variant="outlined"
                  />
                ))}
              </Box>
              
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                统计信息
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    引用次数
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {selectedPaper.citations}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    下载次数
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {selectedPaper.downloads}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails} variant="outlined">
            关闭
          </Button>
          <Button onClick={handleCloseDetails} variant="contained">
            下载PDF
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

// 企业仪表板组件
function EnterpriseDashboard() {
  const [systemMetrics, setSystemMetrics] = React.useState({
    activeAgents: 12,
    totalTasks: 156,
    systemUptime: '99.9%',
    avgResponseTime: '45ms',
    memoryUsage: 68,
    cpuUsage: 42,
    networkLatency: 12,
    errorRate: 0.1
  });

  const [recentActivities, setRecentActivities] = React.useState([
    { id: 1, type: 'task_completed', agent: 'Weather Agent', description: '完成天气数据更新任务', timestamp: '2分钟前', status: 'success' },
    { id: 2, type: 'agent_started', agent: 'Traffic Agent', description: '交通管理智能体启动', timestamp: '5分钟前', status: 'info' },
    { id: 3, type: 'error_occurred', agent: 'Safety Agent', description: '安全检查任务异常', timestamp: '8分钟前', status: 'warning' },
    { id: 4, type: 'task_completed', agent: 'Parking Agent', description: '停车位状态更新完成', timestamp: '12分钟前', status: 'success' },
    { id: 5, type: 'system_alert', agent: 'System', description: '系统性能优化建议', timestamp: '15分钟前', status: 'info' }
  ]);

  const [performanceData, setPerformanceData] = React.useState([
    { time: '00:00', throughput: 120, latency: 45, errors: 0 },
    { time: '04:00', throughput: 95, latency: 52, errors: 1 },
    { time: '08:00', throughput: 180, latency: 38, errors: 0 },
    { time: '12:00', throughput: 220, latency: 42, errors: 2 },
    { time: '16:00', throughput: 195, latency: 48, errors: 1 },
    { time: '20:00', throughput: 160, latency: 41, errors: 0 }
  ]);

  React.useEffect(() => {
    // 模拟实时数据更新
    const interval = setInterval(() => {
      setSystemMetrics(prev => ({
        ...prev,
        totalTasks: prev.totalTasks + Math.floor(Math.random() * 3),
        memoryUsage: Math.max(30, Math.min(90, prev.memoryUsage + (Math.random() - 0.5) * 10)),
        cpuUsage: Math.max(20, Math.min(80, prev.cpuUsage + (Math.random() - 0.5) * 15)),
        networkLatency: Math.max(5, Math.min(50, prev.networkLatency + (Math.random() - 0.5) * 8))
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      case 'info': return 'info';
      default: return 'default';
    }
  };

  const getStatusIcon = (type) => {
    switch (type) {
      case 'task_completed': return <CheckCircleIcon />;
      case 'agent_started': return <PlayIcon />;
      case 'error_occurred': return <CloseIcon />;
      case 'system_alert': return <InfoIcon />;
      default: return <InfoIcon />;
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 700 }}
          >
            企业仪表板
          </Typography>
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ maxWidth: 800, mx: 'auto' }}
          >
            实时监控多智能体DSL框架的系统状态与性能指标
          </Typography>
        </Box>

        {/* System Metrics */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 4 }}>
          系统概览
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <GroupIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {systemMetrics.activeAgents}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  活跃智能体
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <HistoryIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {systemMetrics.totalTasks}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  总任务数
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <CheckCircleIcon sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {systemMetrics.systemUptime}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  系统可用性
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center' }}>
              <CardContent>
                <SettingsIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>
                  {systemMetrics.avgResponseTime}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  平均响应时间
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Performance Metrics */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 4 }}>
          性能指标
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  内存使用率
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ flexGrow: 1, mr: 1 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={systemMetrics.memoryUsage} 
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Typography variant="body2" sx={{ minWidth: 35 }}>
                    {systemMetrics.memoryUsage}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  CPU使用率
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ flexGrow: 1, mr: 1 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={systemMetrics.cpuUsage} 
                      color="secondary"
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Typography variant="body2" sx={{ minWidth: 35 }}>
                    {systemMetrics.cpuUsage}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  网络延迟
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'info.main' }}>
                  {systemMetrics.networkLatency}ms
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  平均网络延迟
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  错误率
                </Typography>
                <Typography variant="h4" sx={{ fontWeight: 700, color: 'error.main' }}>
                  {systemMetrics.errorRate}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  系统错误率
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Recent Activities */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 4 }}>
          最近活动
        </Typography>
        
        <Paper elevation={2}>
          <List>
            {recentActivities.map((activity, index) => (
              <React.Fragment key={activity.id}>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: `${getStatusColor(activity.status)}.main` }}>
                      {getStatusIcon(activity.type)}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {activity.agent}
                        </Typography>
                        <Chip 
                          label={activity.status} 
                          color={getStatusColor(activity.status)}
                          size="small" 
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {activity.description}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {activity.timestamp}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < recentActivities.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>

        {/* Performance Chart */}
        <Typography variant="h4" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 4, mt: 6 }}>
          性能趋势
        </Typography>
        
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              系统吞吐量与延迟趋势
            </Typography>
            <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Typography variant="body1" color="text.secondary">
                性能图表将在此处显示
                <br />
                (需要集成图表库如Recharts)
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
}

// 简化的App组件
function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dsl-demo" element={<DSLDemoPage />} />
          <Route path="/agents" element={<AgentsInterface />} />
          <Route path="/interactions" element={<InteractionHistory />} />
          <Route path="/academic" element={<AcademicPage />} />
          <Route path="/dashboard" element={<EnterpriseDashboard />} />
        </Routes>
      </ThemeProvider>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);