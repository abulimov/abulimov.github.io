Title: About Me


    :::console

    $ whoami
    Alexander Bulimov, Production Engineer from Moscow, Russia

    $ cowsay < about.txt
     _________________________________________
    / DevOps practitioner, fan of Linux, Open \
    | Source and automation of system         |
    | provisioning and orchestration          |
    | processes. Have extensive experience    |
    | and hands-on skill in setting up        |
    | complex web-sites and services for      |
    | web-development. My languages of choice |
    | are Python and Go, and I'm fluent in    |
    \ Bash.                                   /
     -----------------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||

    $ uptime
    {time} up {uptime} days,  1 user,  load average: 0.90, 0.70, 0.50

<!-- script to set time and uptime to real values in output above -->
<script type="text/javascript">
function updateUptime(){
    var today = new Date();
    var minutes = today.getMinutes()
    if (minutes < 10) {
        minutes = "0" + minutes
    }
    var time = today.getHours() + ":" + minutes
    var dateOfBirth = new Date(585864000000);
    var diff = today - dateOfBirth;
    var diffInDays = Math.floor(diff / (24 * 3600 * 1000))
    var highlight = document.getElementsByClassName("highlight")[0];
    highlight.innerHTML = highlight.innerHTML.replace('{uptime}', diffInDays).replace('{time}', time);
}
window.onload = updateUptime
</script>
