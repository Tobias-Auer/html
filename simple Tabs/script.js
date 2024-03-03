var TabBlock = {
    
    init: function() {
      TabBlock.bindUIActions();
    },
    
    bindUIActions: function() {
      $('.tabBlock-tabs').on('click', '.tabBlock-tab', function(){
        TabBlock.switchTab($(this));
      });
    },
    
    switchTab: function($tab) {
      var $context = $tab.closest('.tabBlock');
      
      if (!$tab.hasClass('is-active')) {
        $tab.siblings().removeClass('is-active');
        $tab.addClass('is-active');
      }
     },
  };
  
  $(function() {
    TabBlock.init();
  });