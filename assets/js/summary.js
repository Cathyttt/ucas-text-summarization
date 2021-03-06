// http://10.10.103.47:5000
var app = new Vue({
	el:"#app",
	data: {
		message:""
	},

    methods:{
	    example1:function (){
            var that = this;
            that.message = "State health departments and governors' offices across the country are finally being told by the Centers for Disease Control and Prevention and Operation Warp Speed how many doses of the coronavirus vaccine they will initially be receiving once the vaccine becomes is authorized, and it's not enough.\n" +
                "With the Pfizer vaccine emergency use authorization expected later this month, and perhaps also for the Moderna vaccine, states are learning there's not enough for them to fully vaccinate those designated as their first and top priority.\n" +
                "Earlier this week, the CDC's Advisory Committee on Immunization Practices recommended that the very first batch of Americans to get vaccinated should be frontline health care workers and residents of long term care facilities such as nursing homes. Together, they add up to about 24 million people.\n" +
                "Federal officials estimate about 40 million vaccines will be available by the end of the month if both Moderna and Pfizer get US Food and Drug Administration authorization -- only enough to vaccinate 20 million people, because two doses are needed for each person.\n" +
                "But even that number will fall short. Pfizer is only expected to have 6.4 million doses of vaccine ready by mid-December.";
        },
        example2:function (){
            var that = this;
            that.message = "On Monday, it looked like nothing was going to happen on stimulus. Now, it's possible a deal is brokered in a matter of days.\n" +
                "It's crunch time. If a bipartisan group of lawmakers is actually going to unlock a stimulus agreement and present it in writing by Monday, there is a lot of work left to do.\n" +
                "You saw an avalanche of positive comments coming from Republican senators on Thursday. They were open to this pathway, and that's because it's really the only option on the table right now that could become law\n" +
                "\"I've never been more hopeful that we'll get a bill,\" said Sen. Lindsey Graham, a Republican from South Carolina.\n" +
                "This could change if negotiations break down and leadership gets involved to hash out a smaller deal that simply extends expiring provisions. But Republican members know that their GOP proposal can't earn Democratic support. So, if you are a member who wants an outcome, the best strategy is to try to engage on this proposal. That's what you are seeing right now.\n" +
                "There's a ton of hope, but there still isn't a bill.";
        },

        example3:function (){
            var that = this;
            that.message =  "China's Chang'e-5 probe is preparing for a soft landing on the moon to undertake the country's first collection of samples from an extraterrestrial body.\n" +
                "The lander-ascender combination of the spacecraft separated from its orbiter-returner combination at 4:40 am Monday, according to the China National Space Administration (CNSA).\n" +
                "The spacecraft is performing well and communication with ground control is normal, CNSA said."
        },

         example4:function (){
            var that = this;
            that.message = "US President-elect Joe Biden on Monday unveiled his economic team, nominating Janet Yellen, former Federal Reserve chair, to lead the Treasury Department.\n" +
                "If confirmed by the Senate, Yellen would be the first woman to serve as US treasury secretary in the department's 231 years of history. She would also be the first person to have served as treasury secretary, chair of the Council of Economic Advisers, and chair of the Federal Reserve.\n" +
                "The president-elect also selected Wally Adeyemo, president of the Obama Foundation, as deputy secretary of the Treasury.\n" +
                "If confirmed, Adeyemo would be the first Black deputy secretary of the Treasury.\n" +
                "Biden also selected Neera Tanden, who currently serves as president and CEO of the Center for American Progress, as director of the Office of Management and Budget, and named Cecilia Rouse, dean of the Princeton School of Public and International Affairs, to lead the White House Council of Economic Advisers.";
        },
        example5:function (){
            var that = this;
            that.message = "@人民日报:#马航飞机失联#【马航对“失联航班”持悲观态度】9日上午，马航没有发布失联航班的最新消息，仅是安抚家属们称，目前航班失联已超过30小时，请做好最坏的心理准备。在场许多家属听到这一消息，马上崩溃、大哭。（人民网）祈祷平安，同胞节哀！\n"},
        srnclick:function(){
            $('#json').text("");
            var that = this;
            console.log(that.message);
            console.log("bs");
            axios.post('http://10.10.103.47:5001/summarunner',{text:that.message}).then(function(response){
                console.log(response.data);
                if (response.data.status_code==1) {
                    // var data = JSON.stringify(response.data.summary_content);
                    var data = response.data.summary_content;
                    console.log(data);
                    $('#json').text(data);
                }
                else{
                    alert("Summarize Error!")
                }

            },function(err){
            console.log(err);
             });
        },

        beclick:function(){
            $('#json').text("");
            var that = this;
            console.log(that.message);
            console.log("be");
            axios.post('http://10.10.103.47:5000/bertext',{text:that.message}).then(function(response){
                console.log(response.data);
                if (response.data.status_code==1) {
                    // var data = JSON.stringify(response.data.summary_content);
                    var data = response.data.summary_content;
                    console.log(data);
                    $('#json').text(data);
                }
                else{
                    alert("Summarize Error!")
                }

            },function(err){
            console.log(err);
             });
        },

        pgclick:function(){
            $('#json').text("");
            var that = this;
            console.log(that.message);
            console.log("pg");
            axios.post('http://10.10.103.47:5002/ptrnet',{text:that.message}).then(function(response){
                console.log(response.data);
                if (response.data.status_code==1) {
                    // var data = JSON.stringify(response.data.summary_content);
                    var data = response.data.summary_content;
                    console.log(data);
                    $('#json').text(data);
                }
                else{
                    alert("Summarize Error!")
                }

            },function(err){
            console.log(err);
             });
        },

        baclick:function(){
            $('#json').text("");
            var that = this;
            console.log(that.message);
            console.log("ba");
            axios.post('http://10.10.103.47:5000/bertabs',{text:that.message}).then(function(response){
                console.log(response.data);
                if (response.data.status_code==1) {
                    // var data = JSON.stringify(response.data.summary_content);
                    var data = response.data.summary_content;
                    console.log(data);
                    $('#json').text(data);
                }
                else{
                    alert("Summarize Error!")
                }

            },function(err){
            console.log(err);
             });
        },

        //CQU NLP摘要接口
        cquclick:function(){
            $('#json').text("");
            var that = this;
            console.log(that.message);
             axios.get('http://39.100.48.36:3002/predict_summary?sentence='+that.message).then(function(response){
                console.log(response.data);
                //var data=JSON.stringify(response.data.summary_content);
                var data = response.data.summary_content;
                console.log(typeof(data));
                $('#json').text(data);

        },function(err){
            console.log(err);
             });
        }

    }

})