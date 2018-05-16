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