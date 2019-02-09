// just write something to show everything is working
document.write("should play a sound");
// instantiate audio context and oscillator
const context = new AudioContext();
const oscillator = context.createOscillator();  // oscillator is the audio source
// decide the type of the wave and its frequency (note)
oscillator.type = "sine";
oscillator.frequency.value = 196;
// create gain node
const gainNode = context.createGain();
// context.destination is the audio-rendering device (speakers)
oscillator.connect(gainNode);
gainNode.connect(context.destination);
// play sound
oscillator.start(0);