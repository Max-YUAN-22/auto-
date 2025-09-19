import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { 
  Box, Typography, Container, AppBar, Toolbar, Button, Card, CardContent, 
  Grid, Chip, Paper, Stepper, Step, StepLabel, StepContent, Alert, 
  LinearProgress, Dialog, DialogTitle, DialogContent, DialogActions, 
  IconButton, Avatar, List, ListItem, ListItemAvatar, ListItemText, 
  ListItemSecondaryAction, Switch, FormControlLabel, TextField, Divider, 
  Badge, Tooltip, Fab, Tabs, Tab, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, CardHeader, CardActions, ButtonGroup, Stack
} from '@mui/material';
import { 
  Science as ScienceIcon, Code as CodeIcon, School as SchoolIcon, 
  Dashboard as DashboardIcon, PlayArrow as PlayIcon, CheckCircle as CheckCircleIcon, 
  Close as CloseIcon, Info as InfoIcon, Group as GroupIcon, History as HistoryIcon, 
  Settings as SettingsIcon, Chat as ChatIcon, Send as SendIcon, 
  Visibility as VisibilityIcon, VisibilityOff as VisibilityOffIcon, 
  Refresh as RefreshIcon, Add as AddIcon, Security as SecurityIcon, 
  Speed as SpeedIcon, TrendingUp as TrendingUpIcon, Business as BusinessIcon,
  Cloud as CloudIcon, Storage as StorageIcon, NetworkCheck as NetworkIcon,
  Assessment as AssessmentIcon, Timeline as TimelineIcon, 
  AccountBalance as AccountBalanceIcon, Public as PublicIcon
} from '@mui/icons-material';

// 企业级主题配置
const enterpriseTheme = createTheme({
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
    success: {
      main: '#4caf50',
    },
    warning: {
      main: '#ff9800',
    },
    error: {
      main: '#f44336',
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
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          borderRadius: '12px',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});

// 企业级首页组件
function EnterpriseHomePage() {
  const [activeTab, setActiveTab] = React.useState(0);

  const coreFeatures = [
    {
      title: 'ATSLP算法',
      subtitle: '自适应任务调度与负载预测',
      description: '基于历史模式和智能体专业化的创新调度算法，实现最优任务分配',
      icon: <SpeedIcon sx={{ fontSize: 40 }} />,
      color: 'primary',
      metrics: '2.17x 吞吐量提升',
      features: ['负载预测', '优先级调度', '超时控制', '自适应分配']
    },
    {
      title: 'HCMPL算法',
      subtitle: '分层缓存管理与模式学习',
      description: '使用机器学习技术的智能缓存算法，实现多级缓存管理',
      icon: <TrendingUpIcon sx={{ fontSize: 40 }} />,
      color: 'secondary',
      metrics: '85%+ 缓存命中率',
      features: ['模式学习', '多级缓存', '智能替换', '命中率优化']
    },
    {
      title: 'CALK算法',
      subtitle: '协作智能体学习与知识转移',
      description: '基于能力相似性的知识转移算法，加速学习过程',
      icon: <GroupIcon sx={{ fontSize: 40 }} />,
      color: 'success',
      metrics: '40-60% 延迟减少',
      features: ['知识转移', '协作学习', '性能提升', '经验共享']
    },
  ];

  const enterpriseMetrics = [
    { metric: '2.17x', label: '吞吐量提升', icon: <SpeedIcon />, color: 'primary' },
    { metric: '1000+', label: '智能体支持', icon: <GroupIcon />, color: 'secondary' },
    { metric: '85%+', label: '缓存命中率', icon: <TrendingUpIcon />, color: 'success' },
    { metric: '40-60%', label: '延迟减少', icon: <SecurityIcon />, color: 'warning' },
  ];

  const enterpriseServices = [
    {
      title: '企业级监控',
      description: '实时系统状态监控、性能指标追踪、智能体协作分析',
      icon: <AssessmentIcon />,
      features: ['实时监控', '性能分析', '异常检测', '告警系统']
    },
    {
      title: '安全与合规',
      description: 'API密钥安全管理、数据加密传输、访问权限控制',
      icon: <SecurityIcon />,
      features: ['密钥管理', '数据加密', '权限控制', '审计日志']
    },
    {
      title: '云原生部署',
      description: '支持Kubernetes、Docker容器化、微服务架构',
      icon: <CloudIcon />,
      features: ['容器化', '微服务', '自动扩缩', '负载均衡']
    },
    {
      title: '全球CDN',
      description: '全球内容分发网络，确保低延迟和高可用性',
      icon: <PublicIcon />,
      features: ['全球加速', '边缘计算', '智能路由', '故障转移']
    },
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
            🚀 多智能体DSL框架
          </Typography>
          <Typography
            variant="h5"
            component="h2"
            gutterBottom
            sx={{ opacity: 0.9, mb: 3, textAlign: 'center' }}
          >
            企业级自适应调度与协作学习解决方案
          </Typography>
          <Typography
            variant="body1"
            sx={{ fontSize: '1.1rem', mb: 4, opacity: 0.9, textAlign: 'center', maxWidth: 800, mx: 'auto' }}
          >
            我们提出了一个新颖的多智能体领域特定语言(DSL)框架，通过三个创新算法解决分布式智能体协调的关键挑战：
            ATSLP、HCMPL和CALK算法。
          </Typography>
          
          {/* 企业级状态指示器 */}
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap">
              <Chip 
                label="✅ 企业级部署成功" 
                sx={{ 
                  backgroundColor: 'rgba(255,255,255,0.2)', 
                  color: 'white',
                  fontSize: '1rem',
                  padding: '8px 16px'
                }} 
              />
              <Chip 
                label="🌐 全球CDN加速" 
                sx={{ 
                  backgroundColor: 'rgba(255,255,255,0.2)', 
                  color: 'white',
                  fontSize: '1rem',
                  padding: '8px 16px'
                }} 
              />
              <Chip 
                label="🔒 企业级安全" 
                sx={{ 
                  backgroundColor: 'rgba(255,255,255,0.2)', 
                  color: 'white',
                  fontSize: '1rem',
                  padding: '8px 16px'
                }} 
              />
            </Stack>
            <Typography variant="body2" sx={{ mt: 2, opacity: 0.8 }}>
              部署时间: {new Date().toLocaleString('zh-CN')} | 版本: v2.0.0 Enterprise
            </Typography>
          </Box>
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
            企业级性能指标
          </Typography>
          <Grid container spacing={3}>
            {enterpriseMetrics.map((metric, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Card sx={{ textAlign: 'center', height: '100%' }}>
                  <CardContent>
                    <Box sx={{ color: `${metric.color}.main`, mb: 2 }}>
                      {metric.icon}
                    </Box>
                    <Typography
                      variant="h4"
                      sx={{ fontWeight: 700, color: `${metric.color}.main` }}
                    >
                      {metric.metric}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {metric.label}
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
            {coreFeatures.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardHeader
                    avatar={
                      <Avatar sx={{ bgcolor: `${feature.color}.main` }}>
                        {feature.icon}
                      </Avatar>
                    }
                    title={
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {feature.title}
                      </Typography>
                    }
                    subheader={feature.subtitle}
                  />
                  <CardContent>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {feature.description}
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      {feature.features.map((feat, idx) => (
                        <Chip
                          key={idx}
                          label={feat}
                          size="small"
                          variant="outlined"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
                    </Box>
                    <Chip
                      label={feature.metrics}
                      color={feature.color}
                      size="small"
                      sx={{ fontWeight: 600 }}
                    />
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Enterprise Services */}
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            component="h2"
            gutterBottom
            sx={{ textAlign: 'center', fontWeight: 600, mb: 4 }}
          >
            企业级服务
          </Typography>
          <Grid container spacing={3}>
            {enterpriseServices.map((service, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                        {service.icon}
                      </Avatar>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {service.title}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {service.description}
                    </Typography>
                    <Box>
                      {service.features.map((feature, idx) => (
                        <Chip
                          key={idx}
                          label={feature}
                          size="small"
                          variant="outlined"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
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
            立即体验企业级技术
          </Typography>
          <Typography
            variant="body1"
            color="text.secondary"
            sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}
          >
            通过我们的交互式演示，深入了解多智能体DSL框架的强大功能和创新算法
          </Typography>
          <ButtonGroup variant="contained" size="large">
            <Button startIcon={<CodeIcon />} sx={{ px: 4 }}>
              开始DSL演示
            </Button>
            <Button startIcon={<ScienceIcon />} sx={{ px: 4 }}>
              查看学术论文
            </Button>
            <Button startIcon={<BusinessIcon />} sx={{ px: 4 }}>
              企业咨询
            </Button>
          </ButtonGroup>
        </Box>
      </Container>
    </Box>
  );
}

// 企业级导航栏
function EnterpriseNavigation() {
  const navigate = React.useNavigate();
  
  return (
    <AppBar position="sticky" elevation={2}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <ScienceIcon sx={{ fontSize: 32 }} />
          <Typography variant="h5" component="h1" sx={{ fontWeight: 700 }}>
            多智能体DSL框架
          </Typography>
          <Chip label="企业版" color="secondary" size="small" />
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

// 企业级App组件
function EnterpriseApp() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={enterpriseTheme}>
        <CssBaseline />
        <EnterpriseNavigation />
        <Routes>
          <Route path="/" element={<EnterpriseHomePage />} />
          <Route path="/dsl-demo" element={<EnterpriseHomePage />} />
          <Route path="/agents" element={<EnterpriseHomePage />} />
          <Route path="/interactions" element={<EnterpriseHomePage />} />
          <Route path="/academic" element={<EnterpriseHomePage />} />
          <Route path="/dashboard" element={<EnterpriseHomePage />} />
        </Routes>
      </ThemeProvider>
    </BrowserRouter>
  );
}

// 渲染企业级应用
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <EnterpriseApp />
  </React.StrictMode>
);
