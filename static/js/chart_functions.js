// import Chart from 'chart.js/auto'


function generate_activity_bar_chart(){
    data_dict = activity_bar_chart_data
    data_arr = []
    labels = []
    for (const key in data_dict){
        data_arr.push(data_dict[key])
        labels.push(key)
    }
    const data = {
        labels: labels, 
        datasets: [{
            label: "Number of responses", 
            data: data_arr, 
            backgroundColor: [
                "rgba(255, 99, 132, 0.2)"
            ]
        }]
    }
    const config = {
        type: 'bar',
        data: data,
        options: {
          scales: {

            y: [{
              ticks: {
                precision: 0, 
                stepSize: 1
              }
            }]
          }
        },
    };
    const ctx = document.getElementById("barChart1")
    const myBarChart = new Chart(ctx, config)

}


function generate_time_spent_bar_chart(){
    data_dict = time_spent_bar_chart
    data_arr = []
    labels = []
    for (const key in data_dict){
        data_arr.push(data_dict[key])
        labels.push(key)
    }
    const data = {
        labels: labels, 
        datasets: [{
            label: "Number of responses",
            data: data_arr, 
            backgroundColor: [
                "rgba(39, 153, 245, 0.8)"
            ]
        }]
    }
    const config = {
        type: 'bar',
        data: data,
        options: {
          scales: {

            y: [{
              ticks: {
                precision: 0, 
                stepSize: 1
              }
            }]
          }
        },
    };
    const ctx = document.getElementById("barChart2")
    const myBarChart = new Chart(ctx, config)

}

function generate_time_series_chart(){
  data_dict = survey_count_data
  console.log(data_dict)
  data_arr = []
    labels = []
    for (const key in data_dict){
        data_arr.push(data_dict[key])
        labels.push(key)
    }
    console.log(labels)

    const data = {
      labels: labels, 
      datasets: [{
        label: 'Number of Survey Submissions', 
        data: data_arr, 
        fill: false, 
        borderColor: 'rgb(75,192,192)',
        tension: 0, 
        showLine: true


      }]
    }
    var ctx = document.getElementById("lineChart1")
    const chart = new Chart(ctx, {
      type: 'line', 
      data: data,
      options: {
          scales: {

            y: [{
              ticks: {
                callback: function(value){if (value % 1 === 0) {return value}}, 
                precision: 0, 
                stepSize: 1
              }
            }]
          }
        },
    })

}

async function generate_charts(){
  await generate_activity_bar_chart()
  await generate_time_spent_bar_chart()
  await generate_time_series_chart()

}

window.onload = generate_charts


