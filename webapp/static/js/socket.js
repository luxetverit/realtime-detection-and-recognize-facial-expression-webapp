const video = document.getElementById('video');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const anger= document.getElementById('anger')
const anxiety= document.getElementById('anxiety')
const embarrassed= document.getElementById('embarrassed')
const hurt= document.getElementById('hurt')
const neutral= document.getElementById('neutral')
const pleasure= document.getElementById('pleasure')
const sad= document.getElementById('sad')
let chartdata=[]
var context = document
.getElementById('myChart')
.getContext('2d');
var myChart = new Chart(context, {
type: 'bar', // 차트의 형태
data: { // 차트에 들어갈 데이터
    labels: [
        //x 축
        'anger','anxiety','embarrassed','hurt','neutral','pleasure','sad'
    ],
    datasets: [
        { //데이터
            label: '감정차트', //차트 제목
            fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
            data:[0,0,0,0,0,0,0] ,
            backgroundColor: [
                //색상
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                //경계선 색상
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1 //경계선 굵기
        }/* ,
        {
            label: 'test2',
            fill: false,
            data: [
                8, 34, 12, 24
            ],
            backgroundColor: 'rgb(157, 109, 12)',
            borderColor: 'rgb(157, 109, 12)'
        } */
    ]
},
options: {
    scales: {
        yAxes: [
            {
                ticks: {
                    beginAtZero: true
                }
            }
        ]
    }
}
}); 



let socket;

function createWebSocket(counselingId) {
  let socketProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
  let socketUrl = socketProtocol + window.location.host + '/ws/video/' + counselingId + '/';
  socket = new WebSocket(socketUrl);

  socket.onopen = function(event) {
    console.log('WebSocket opened:', event);
  };

  socket.onmessage = function(event) {
    data=JSON.parse(event.data)
    const imageBase64 = data['image'];
    const feelings = data['feelings'];
    
    anger.innerText= feelings['anger'];
    anxiety.innerText= feelings['anxiety'];
    embarrassed.innerText= feelings['embarrassed'];
    hurt.innerText= feelings['hurt'];
    neutral.innerText= feelings['neutral'];
    pleasure.innerText= feelings['pleasure'];
    sad.innerText= feelings['sad'];
    chartdata = [
    parseInt(feelings['anger']),
    parseInt(feelings['anxiety']),
    parseInt(feelings['embarrassed']),
    parseInt(feelings['hurt']),
    parseInt(feelings['neutral']),
    parseInt(feelings['pleasure']),
    parseInt(feelings['sad']),

  ];
  myChart.data.datasets[0].data = chartdata;
  myChart.update();  // 이건 chat.js 에서 제공하는 update 이거땜에 4시간 돌아감 이제 데이터 업데이트 될시 작업 가능 



    video.src = 'data:image/jpeg;base64,' + imageBase64;
  };

  socket.onclose = function(event) {
    console.log('WebSocket closed:', event);
    if (!event.wasClean) {
      setTimeout(createWebSocket(counselingId), 1000);
    }
  };
}

// createWebSocket();

startBtn.addEventListener('click', () => {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    createWebSocket(counselingId);
    setTimeout(() => {
      socket.send('start');
    }, 1000);
  }
  else{
    setTimeout(() => {
      socket.send('start');
    }, 500);
  }
  
});

stopBtn.addEventListener('click', () => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send('stop');
    socket.close(1000);
  
  }
});

window.onbeforeunload = function() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send('stop');
    socket.close(1000);
  }
};


