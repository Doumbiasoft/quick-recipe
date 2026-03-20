'use strict';
(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
         /*------------------
            Product filter
        --------------------*/
        if ($('#category-filter').length > 0) {
            const containerEl = document.querySelector('#category-filter');
            let mixer = mixitup(containerEl, {
                load: {
                    filter: '.mostpopular'
                }
            });
        }
        $(".categories-filter-section .filter-item ul li").on('click', function () {
            $(".categories-filter-section .filter-item ul li").removeClass('active');
            $(this).addClass('active');
        });

        
    });
    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        const bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    $('.set-html').each(function () {
        const html = $(this).data('html');
        $(this).html(html)
    });

    $('.set-limit').each(function () {
        const html = $(this).data('html');
        const length = 100;
        let trimmedString = html.substring(0, length)+"...";
        $(this).html(trimmedString)
    });




    // Search model
	$('.search-switch').on('click', function() {
		$('.search-model').fadeIn(400);
	});

	$('.search-close-switch').on('click', function() {
		$('.search-model').fadeOut(400,function(){
			$('#search-input').val('');
		});
	});


    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-------------------
		Category Select
	--------------------- */
    $('#category').niceSelect();

    /*-------------------
		Local Select
	--------------------- */
    $('#tag').niceSelect();

    $("#scrollToTopBtn").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
     });

})(jQuery);

function aJaxSubmitloading(){
    const $loading = $('.Divloading').hide();
    $("form").on("submit", function (e) {
        $loading.show();
    });
}
$(document).ready(function () {
    aJaxSubmitloading();
});

// Get the button
let mybutton = document.getElementById("scrollToTopBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > (document.body.scrollHeight/3) || document.documentElement.scrollTop > (document.body.scrollHeight/3)) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
function hide(elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
      elements[index].style.display = 'none';
  }
}
function show(elements, specifiedDisplay) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
      elements[index].style.display = specifiedDisplay || 'block';
  }
}
const url_post = $("#url-post").data('url-post');
const url_callback = $("#url-callback").data('url-callback');
const logout_url = $("#logout-url").data('logout-url');
const home_url = $("#home-url").data('home-url');
const auth_url = $("#auth-url").data('auth-url');
const pin_url = $("#pin-url").data('pin-url');
const edit_user_info_url = $("#edit-user-info-url").data('edit-user-info-url');
const user_check_current_pass_url = $("#user-check-current-pass-url").data('user-check-current-pass-url');
const edit_user_password_url = $("#edit-user-password-url").data('edit-user-password-url');
const delete_user_account_url = $("#delete-user-account-url").data('delete-user-account-url');

const app_bootstrap_css_url = $("#app-bootstrap-css-url").data('app-bootstrap-css-url');
const app_main_css_url = $("#app-main-css-url").data('app-main-css-url');


$(".recipe-detail").on("click", async function (e) {
    e.preventDefault();
    const recipe_item = $(this).data('obj');
    const recipe_id = recipe_item.id;
    await axios({
        url: url_post,
        method: "POST",
        data: JSON.stringify(recipe_item),
      }).then(function (response) {
        if(response.data == "success"){
            window.location = `${url_callback}/${recipe_id}`;
        }
      });
});
$(".logout").on("click", async function (e) {
    e.preventDefault();
    await axios({
        url: logout_url,
        method: "POST",
      }).then(function (response) {
        if(response.data == "success"){
            window.location = auth_url;
        }
      });
});

$(".pin-recipe").on("click", async function (e) {
    e.preventDefault();
    const recipe_item = $(this).data('obj');
    await axios({
        url: pin_url,
        method: "POST",
        data: recipe_item,
      }).then(function (response) {
        if(response.data == "success"){
            window.location.reload();
        }
      });
});


$(".infoModal").on("click", async function (e) {
    e.preventDefault();
    const data_first_name = $(this).data('first-name');
    const data_last_name = $(this).data('last-name');
    const $first_name = $("#first_name");
    const $last_name = $("#last_name");
    const $msg_info = $("#msg_info");
    $msg_info.html("");
    $first_name.val(data_first_name);
    $last_name.val(data_last_name);

});

$(".deleteModal").on("click", async function (e) {
  e.preventDefault();

  const $email = $("#email");
  const $msg_delete = $("#msg_delete");
   $msg_delete.html("");
   $email.val("");
   const $delete_account= $(".delete-account");
   $delete_account.attr("disabled",true);


});

$(".edit-user-info").on("click", async function (e) {
    e.preventDefault();

    const first_name = $("#first_name").val();
    const last_name = $("#last_name").val();
    const $msg_info = $("#msg_info");
    let user={};
    $msg_info.html("");

    msg_info
    if (first_name === "" || last_name ===""){
          $msg_info.html("All fields are required*");
        return;
    }
    user.first_name = first_name;
    user.last_name = last_name;

    await axios({
        url: edit_user_info_url,
        method: "POST",
        data: user,
      }).then(function (response) {
        if(response.data == "success"){
            window.location.reload();
        }
      });
});

$(".old_pass").on("blur", async function(e){
  e.preventDefault();

  const $old_pass = $("#old_pass");
  const $new_pass = $("#new_pass");
  const $conf_new_pass = $("#conf_new_pass");

  const $ok_current_pass = $("#ok-current-pass");
  const $nonok_current_pass = $("#nonok-current-pass");

  const $ok_new_pass = $("#ok-new-pass");
  const $nonok_new_pass = $("#nonok-new-pass");

  const $msg_password = $("#msg_password");

  if ($old_pass.val() == ""){
      hide($ok_current_pass);
      hide($nonok_current_pass);
     return;
  }

  await axios({
      url: user_check_current_pass_url,
      method: "POST",
      data: {"curr_password": $old_pass.val()},
    }).then(function (response) {
      if(response.data == "success"){

          hide($nonok_current_pass);
          show($ok_current_pass);
          $new_pass.attr("disabled",false);
          $conf_new_pass.attr("disabled",false);
      }
      if(response.data == "failed"){

          show($nonok_current_pass);
          hide($ok_current_pass);
          $new_pass.val("");
          $conf_new_pass.val("");
          $new_pass.attr("disabled",true);
          $conf_new_pass.attr("disabled",true);
          hide($ok_new_pass);
          hide($nonok_new_pass);
          $msg_password.html("");

      }
    });

});


$(".passwordModal").on("click", function(e){
  e.preventDefault();

  const $old_pass = $("#old_pass");
  const $new_pass = $("#new_pass");
  const $conf_new_pass = $("#conf_new_pass");

  const $ok_current_pass = $("#ok-current-pass");
  const $nonok_current_pass = $("#nonok-current-pass");
  const $ok_new_pass = $("#ok-new-pass");
  const $nonok_new_pass = $("#nonok-new-pass");

  const $msg_password = $("#msg_password");

  $msg_password.html("");
  $old_pass.val("");
  $new_pass.val("");
  $conf_new_pass.val("");

  hide($ok_current_pass);
  hide($nonok_current_pass);
  hide($ok_new_pass);
  hide($nonok_new_pass);

});



$(".conf_new_pass").on("blur", function(e){
  e.preventDefault();

  const $new_pass = $("#new_pass");
  const $conf_new_pass = $("#conf_new_pass");

  const $ok_new_pass = $("#ok-new-pass");
  const $nonok_new_pass = $("#nonok-new-pass");
  const $msg_password = $("#msg_password");

  $msg_password.html("");

  if ($new_pass.val() == "" || $conf_new_pass.val() == ""){
        hide($ok_new_pass);
        hide($nonok_new_pass);
   return;
  }
    if ($conf_new_pass.val().length < 4 ){

        $msg_password.html("Your new password should be at least 4 characters long!");
        hide($ok_new_pass);
        hide($nonok_new_pass);
        return;

      }else{

        $msg_password.html("");
        hide($ok_new_pass);
        hide($nonok_new_pass);

      }

  if ($new_pass.val() == $conf_new_pass.val()){

      show($ok_new_pass);
      hide($nonok_new_pass);

  }else{

      hide($ok_new_pass);
      show($nonok_new_pass);
      return;
  }

});

$(".edit-password").on("click", async function (e) {
  e.preventDefault();

  const $conf_new_pass = $("#conf_new_pass");

  let user={};

  user.new_password = $conf_new_pass.val();

  await axios({
      url: edit_user_password_url,
      method: "POST",
      data: user,
    }).then(function (response) {
      if(response.data == "success"){
          window.location.reload();
      }
    });
});

$(".email").on("blur", function(e){
  e.preventDefault();

  const user_email = $(this).data('email');
  const $email = $("#email");
  const $msg_delete = $("#msg_delete");
  const $delete_account= $(".delete-account");


  if($email.val() == "" ){
     $delete_account.attr("disabled",true);
     $msg_delete.html("");
    return;
  }

  if ($email.val() != user_email){
      $delete_account.attr("disabled",true);
      $msg_delete.html("this email is not your account email");
   return;
  }else{
       $delete_account.attr("disabled",false);
       $msg_delete.html("");
  }


});

$(".delete-account").on("click", async function () {

  const $email = $("#email");
  let user={};
  user.email = $email.val();

  await axios({
      url: delete_user_account_url,
      method: "POST",
      data: user,
    }).then(function (response) {
      if(response.data == "success"){
          window.location.reload();
      }
    });
});
// print pdf
$("#print-pdf").on("click", function () {

      const $video=$("#video");
      const $link_feature=$("#link_feature");
      const $social_media=$("#social_media");

      hide($video);
      hide($link_feature);
      hide($social_media);
      const pdf_name = $(this).data('pdf-name');
      const divContents = $("#page_print").html();
      show($video);
      show($link_feature);
      show($social_media);
      const printWindow = window.open('', '', 'height=400,width=800');
      printWindow.document.write(`<html><head><title>${pdf_name}</title>`);
      printWindow.document.write(`<link rel="stylesheet" href="${app_bootstrap_css_url}" />`);
      printWindow.document.write(`<link rel="stylesheet" href="${app_main_css_url}" />`);
      printWindow.document.write('</head><body>');
      printWindow.document.write(divContents);
      printWindow.document.write('</body></html>');
      printWindow.document.close();
      printWindow.print();

});
