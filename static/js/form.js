$(function() {

    $('#login-form-link').click(function(e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function(e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

});

$(function () {
    $('.button-checkbox').each(function () {

        // Settings
        var $widget = $(this),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'fa fa-check-square-o'
                },
                off: {
                    icon: 'fa fa-square-o'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .removeClass('btn-default')
                    .addClass('btn-' + color + ' active');
            }
            else {
                $button
                    .removeClass('btn-' + color + ' active')
                    .addClass('btn-default');
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i>');
            }
        }
        init();
    });
});


/* Options */
$(document).ready(function() {
    
    var i = 0;
    var row = $("#tab_logic tr").eq(1);
    row.removeClass('hidden').remove();


    function setRow(row, i) {
        
        row.find("select, input, textarea").each(function(){
        
            var name = $(this).attr('name').replace(/-[0-9]+-/, '-'+i+'-');
            var id = $(this).attr('id').replace(/-[0-9]+-/, '-'+i+'-');
            $(this).attr('name', name);
            $(this).attr('id', id);
        
        });

        $('#id_materiallist_set-TOTAL_FORMS').val(i+1);
    }

    var startRow = row.clone();
    setRow(startRow, i);
    $("#tab_logic").append(startRow);
    i++;

    $("#add_row").on("click", function() {
        // Dynamic Rows Code
        
        var _row = row.clone()
        setRow(_row, i);
        
        _row.find('.row-remove').click(function(){
           
           _row.remove();
           $("#tab_logic tr").each(function(i){
              if(i>0)
                setRow($(this), i-1);
           });

        });

        $("#tab_logic").append(_row);
        i++;

  });
});
/******************/


/************************************************
      1 ) Show Meal Attribute
      2 ) Account Settings Page => Home Page 
      3 ) Favourite Attribute
      4 ) Select All Attribute
*************************************************/

$(document).on('click', '.meal', function (){
    url = "/home/meal/"+$(this).attr('id');
    window.location = url;

});


$(document).on('click', '#account-close', function (){
   
        url = "/home/";
        window.location = url;

});


$(document).on('click', '.star', function (){
            
    var meal_id = $(this).attr('id');  
    var url = "/home/favourite/toggle/"+meal_id;  
    var self = this;

    $.ajax({
        url: url,
        }).done(function(res) {
            
            var value = parseInt($(self).find("span").text());

            if(res == "Sub")
            {
                $(self).removeClass('fa-star').addClass('fa-star-o');
                $(self).find("span").text((value-1).toString());
            }
            else
            {
                $(self).removeClass('fa-star-o').addClass('fa-star');
                $(self).find("span").text((value+1).toString());
            }
    });

});
/*************************/


/* Select All Attribute */
$(document).ready(function() {
   $('#selectall').change(function(event) {  //on click
       if(this.checked) { // check select status
           $(".checkbox_container").prop("checked", true);
       }else{
           $(".checkbox_container").prop("checked", false);
       }
   });
});
/*************************/


/* Search Attribute */
$(function () {
    $('a[href="#search"]').on('click', function(event) {
        event.preventDefault();
        $('#search').addClass('open');
        $('#search > form > input[type="search"]').focus();
    });
    
    $('#search, #search button.close').on('click keyup', function(event) {
        if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
            $(this).removeClass('open');
        }
    });
});
/********************/


/* Crop User Image */
function cropUserImage(image) {
    $('.image-editor').cropit('destroy');
    $('.image-editor').cropit({
        imageState: { src: image }
        }
    );

    $('#myModal').modal('show');

    $('.export').click(function(e) {
        //e.preventDefault();
        var imageData = $('.image-editor').cropit('export');

        $('#hidden_field').val(imageData);
    });
}

function choiceUserImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            cropUserImage(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function(){
    $("#change_image").change(function () {
        choiceUserImage(this);
    });
});
/********************/


/* Crop Meal Image */
function cropMealImage(image) {
    $('.image-editor').cropit('destroy');
    $('.image-editor').cropit({
        imageState: { src: image }
    });

    $('#myModal').modal('show');

    $('.export').click(function(e) {
        e.preventDefault();
        var imageData = $('.image-editor').cropit('export');

        $('#prevMeal').attr('src', imageData);
        $('#meal_hidden').val(imageData);
        $('#myModal_close').click();

    });
}

function choiceMealImage(input) {
     if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            cropMealImage(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function(){
    $("#meal_image").change(function () {
        choiceMealImage(this);
    });
});
/**************************/

//$('.selectpicker').selectpicker();
