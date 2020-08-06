import tensorflow as tf

SIZE = 28
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = 1 - x_train.reshape(-1, SIZE * SIZE) / 255.0
x_test = 1 - x_test.reshape(-1, SIZE * SIZE) / 255.0

model = tf.keras.models.Sequential([
  tf.keras.Input(shape=(SIZE * SIZE,)),
  tf.keras.layers.Dense(128, activation='relu',),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10),
  tf.keras.layers.Softmax()
])
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10)
test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
print('Test accuracy:', test_acc)
model.save('model')
