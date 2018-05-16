/* ===== Logic for creating fake Select Boxes ===== */
$(document).ready(function () {
  console.log("ready!");
  $('.sel').each(function () {
    $(this).children('select').css('display', 'none');

    var $current = $(this);

    $(this).find('option').each(function (i) {
      if (i == 0) {
        $current.prepend($('<div>', {
          class: $current.attr('class').replace(/sel/g, 'sel__box')
        }));

        var placeholder = $(this).text();
        $current.prepend($('<span>', {
          class: $current.attr('class').replace(/sel/g, 'sel__placeholder'),
          text: placeholder,
          'data-placeholder': placeholder
        }));

        return;
      }

      $current.children('div').append($('<span>', {
        class: $current.attr('class').replace(/sel/g, 'sel__box__options'),
        text: $(this).text()
      }));
    });
  });

  // Toggling the `.active` state on the `.sel`.
  $('.sel').click(function () {
    $(this).toggleClass('active');
  });

  // Toggling the `.selected` state on the options.
  $('.sel__box__options').click(function () {
    var txt = $(this).text();
    var index = $(this).index();

    $(this).siblings('.sel__box__options').removeClass('selected');
    $(this).addClass('selected');

    var $currentSel = $(this).closest('.sel');
    $currentSel.children('.sel__placeholder').text(txt);
    $currentSel.children('select').prop('selectedIndex', index + 1);
  });
  function loginSkinImage(name, directory, callback) {
    var dir = directory;
    var img = new Image();
    var url = dir + "/" + name + ".png";
    img.onload = function () {
      callback(img);
    };
    img.src = url;
  }
  function skinsForLoad(skinName) {
    loginSkinImage(skinName, "characters", function (image) {
      $(image).attr("id", skinName);
      $('#gameSource').append(image);
    });
  }

  var loginJson = function () {
    $.ajaxSetup({
      async: false
    });
    var jsonTemp = null;
    $.getJSON("loaders.json", function (data) {
      jsonTemp = data;
    });
    return jsonTemp;
  }();
  var dizi = [];
  var jsonLoginData = loginJson;
  for (var k in jsonLoginData.characters) {

    dizi.push(jsonLoginData.characters[k].skin + "S0");
    console.log(jsonLoginData.characters[k].skin + "S0");
    skinsForLoad(jsonLoginData.characters[k].skin + "S0");

  }
  var sayac = 0;
  var url = "characters/";
  function setSRC() {

    url += dizi[sayac] + ".png";
    $("#skinImage").attr('src', url);
    url = "characters/";
  }
  $("#btnPrev").click(function () {

    if (sayac > 0) {
      sayac--;
      setSRC();
    }
    else {
      sayac = dizi.length - 1;
      setSRC();
    }
  });
  $("#btnNext").click(function () {
    if (sayac == dizi.length - 1) {
      sayac = 0;
      setSRC();
    }
    else {
      sayac++;
      setSRC();
    }
  });
  function redirect(url) {
    var ua = navigator.userAgent.toLowerCase(),
      isIE = ua.indexOf('msie') !== -1,
      version = parseInt(ua.substr(4, 2), 10);

    // Internet Explorer 8 and lower
    if (isIE && version < 9) {
      var link = document.createElement('a');
      link.href = url;
      document.body.appendChild(link);
      link.click();
    }

    // All other browsers can use the standard window.location.href (they don't lose HTTP_REFERER like Internet Explorer 8 & lower does)
    else {
      window.location.href = url;
    }
  }
  $("#giris").click(function () {
    // console.log(dizi[sayac]);
    var nick = $("#txtNick").val();
    var skin = dizi[sayac];
    $.cookie("nick", nick, { expires: 7 });
    $.cookie("skin", skin.substring(0, skin.length - 2), { expires: 7 });

    console.log(skin.substring(0, skin.length - 2), nick);

    var loc = "index.html"; // or a new URL
    window.location.href = loc + '?refresh=true'; // random number

   // redirect("index.html");
  });
});
