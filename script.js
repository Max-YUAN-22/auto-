// Multi-Agent DSL Framework - Web Demo JavaScript

// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.navbar a');
    const sections = document.querySelectorAll('.section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Show corresponding section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
    
    // Initialize components
    initializeDSLEditor();
    initializeMonitoring();
    initializePerformanceChart();
    initializeAgentStatus();
});

// DSL Editor functionality
function initializeDSLEditor() {
    const editor = document.getElementById('dsl-editor');
    const output = document.getElementById('output');
    const runBtn = document.getElementById('run-btn');
    const clearBtn = document.getElementById('clear-btn');
    
    runBtn.addEventListener('click', function() {
        const code = editor.value;
        if (code.trim()) {
            executeDSLProgram(code);
        }
    });
    
    clearBtn.addEventListener('click', function() {
        output.innerHTML = '';
    });
}

function executeDSLProgram(code) {
    const output = document.getElementById('output');
    
    // Simulate DSL execution
    output.innerHTML = '<div class="execution-log">Executing DSL program...</div>';
    
    setTimeout(() => {
        const lines = code.split('\n');
        let log = '<div class="execution-log">';
        
        lines.forEach((line, index) => {
            if (line.trim() && !line.startsWith('#')) {
                log += `<div class="log-line">[${index + 1}] ${line.trim()}</div>`;
            }
        });
        
        log += '<div class="log-success">✓ DSL program executed successfully!</div>';
        log += '<div class="log-info">Generated 3 agents: traffic_manager, traffic_monitor, route_optimizer</div>';
        log += '<div class="log-info">Created contract: traffic_management</div>';
        log += '<div class="log-info">Executed traffic_analysis_task with SLA compliance</div>';
        log += '</div>';
        
        output.innerHTML = log;
    }, 1000);
}

// Monitoring functionality
function initializeMonitoring() {
    // Simulate real-time updates
    setInterval(updateMetrics, 2000);
}

function updateMetrics() {
    // Simulate metric updates
    const throughput = document.getElementById('throughput');
    const memory = document.getElementById('memory');
    const successRate = document.getElementById('success-rate');
    const latency = document.getElementById('latency');
    
    // Add slight variations to simulate real-time data
    const baseThroughput = 10.09;
    const variation = (Math.random() - 0.5) * 0.5;
    throughput.textContent = (baseThroughput + variation).toFixed(2);
    
    // Memory with slight variation around 0.94 MB
    const baseMemory = 0.94;
    const memoryVariation = (Math.random() - 0.5) * 0.1;
    memory.textContent = (baseMemory + memoryVariation).toFixed(2);
    
    // Success rate stays at 100%
    successRate.textContent = '100';
    
    // Latency with slight variation around 98.98 ms
    const baseLatency = 98.98;
    const latencyVariation = (Math.random() - 0.5) * 5;
    latency.textContent = (baseLatency + latencyVariation).toFixed(2);
}

// Agent status functionality
function initializeAgentStatus() {
    const agentList = document.getElementById('agent-list');
    
    const agents = [
        { name: 'traffic_manager', status: 'online', load: 0.65 },
        { name: 'traffic_monitor', status: 'online', load: 0.42 },
        { name: 'route_optimizer', status: 'online', load: 0.38 },
        { name: 'emergency_handler', status: 'online', load: 0.15 },
        { name: 'data_analyzer', status: 'online', load: 0.73 }
    ];
    
    function updateAgentStatus() {
        agentList.innerHTML = '';
        
        agents.forEach(agent => {
            const agentElement = document.createElement('div');
            agentElement.className = `agent-item ${agent.status}`;
            agentElement.innerHTML = `
                <div class="agent-name">${agent.name}</div>
                <div class="agent-load">Load: ${(agent.load * 100).toFixed(1)}%</div>
                <div class="agent-status-indicator">${agent.status}</div>
            `;
            agentList.appendChild(agentElement);
        });
    }
    
    updateAgentStatus();
    setInterval(updateAgentStatus, 3000);
}

// Performance chart functionality
function initializePerformanceChart() {
    const ctx = document.getElementById('performance-chart').getContext('2d');
    
    const performanceData = {
        labels: ['LangChain', 'CrewAI', 'AutoGen', 'Our DSL'],
        datasets: [{
            label: 'Throughput (tasks/sec)',
            data: [0.78, 0.86, 0.88, 1.66],
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 2
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: performanceData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Throughput (tasks/sec)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Framework'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Performance Comparison Across Frameworks'
                },
                legend: {
                    display: false
                }
            }
        }
    });
}

// Example loading functionality
function loadExample(type) {
    const editor = document.getElementById('dsl-editor');
    
    const examples = {
        traffic: `# Traffic Management Example
spawn traffic_manager {
    capabilities: ["traffic_analysis", "route_optimization"]
    load_threshold: 0.8
}

spawn traffic_monitor {
    capabilities: ["real_time_monitoring", "incident_detection"]
    load_threshold: 0.7
}

contract traffic_management {
    parties: [traffic_manager, traffic_monitor]
    sla: { response_time: "500ms", availability: "99.9%" }
}

route traffic_analysis_task to traffic_manager
with_sla { max_latency: "300ms", retry_count: 3 }

gather results from [traffic_manager, traffic_monitor]
on completion { emit traffic_analysis_complete(results) }`,
        
        healthcare: `# Healthcare Coordination Example
spawn patient_coordinator {
    capabilities: ["patient_care", "resource_allocation"]
    load_threshold: 0.7
}

spawn medical_scheduler {
    capabilities: ["appointment_scheduling", "resource_booking"]
    load_threshold: 0.6
}

contract healthcare_coordination {
    parties: [patient_coordinator, medical_scheduler]
    sla: { response_time: "200ms", availability: "99.95%" }
}

route patient_care_task to patient_coordinator
with_sla { max_latency: "150ms", retry_count: 5 }

gather results from [patient_coordinator, medical_scheduler]
on completion { emit patient_care_complete(results) }`,
        
        smartcity: `# Smart City Management Example
spawn infrastructure_monitor {
    capabilities: ["infrastructure_monitoring", "maintenance_scheduling"]
    load_threshold: 0.8
}

spawn service_coordinator {
    capabilities: ["service_coordination", "resource_management"]
    load_threshold: 0.7
}

contract smart_city_management {
    parties: [infrastructure_monitor, service_coordinator]
    sla: { response_time: "1000ms", availability: "99.8%" }
}

route infrastructure_task to infrastructure_monitor
with_sla { max_latency: "800ms", retry_count: 2 }

gather results from [infrastructure_monitor, service_coordinator]
on completion { emit infrastructure_update_complete(results) }`
    };
    
    if (examples[type]) {
        editor.value = examples[type];
        // Switch to editor tab
        document.querySelector('a[href="#editor"]').click();
    }
}

// Add some CSS for execution logs
const style = document.createElement('style');
style.textContent = `
    .execution-log {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .log-line {
        color: #333;
        margin: 2px 0;
    }
    
    .log-success {
        color: #28a745;
        font-weight: bold;
        margin: 10px 0 5px 0;
    }
    
    .log-info {
        color: #17a2b8;
        margin: 2px 0;
    }
    
    .agent-name {
        font-weight: bold;
        color: #333;
    }
    
    .agent-load {
        color: #666;
        font-size: 0.9rem;
    }
    
    .agent-status-indicator {
        color: #28a745;
        font-weight: bold;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    .agent-item.offline .agent-status-indicator {
        color: #dc3545;
    }
`;
document.head.appendChild(style);
