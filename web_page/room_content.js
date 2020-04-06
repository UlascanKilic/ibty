function RoomContent(id, textureName, posX, posY, contentType){
  this.id = id;
  this.positionX = posX;
  this.positionY = posY;
  this.textureName = textureName;
  this.textureSourceElement;
  this.contentType = contentType;

  this.updateTextureSourceElement = function() {
    this.textureSourceElement = $('#texture_' + this.contentType + '_' + this.textureName)[0];
  };
}


//https://www.youtube.com/watch?v=3EMxBkqC4z0&list=PLnZAnn3DFwB7NUAVwD02vEVVfjNbWwCRW&index=4&t=1031s