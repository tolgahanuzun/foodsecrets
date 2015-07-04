
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
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
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
