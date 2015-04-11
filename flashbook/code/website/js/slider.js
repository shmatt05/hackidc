

$(document).ready(function(){
    $('#dater-duration').jRange({
        from: 0,
        to: 100,
        step: 1,
        scale: [0,25,50,75,100],
        format: '%s',
        width: 270,
        showLabels: true,
        isRange : true
    });
    //console.log($('#dater-duration'));
    //console.log($('#dater-duration').val());
});
