import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def num():
    a = np.zeros((2, 2))
    b = np.ones((2, 2))
    print(a)
    print(b)
    print(np.sum(b, axis=1))  # 1是行相加，0是列相加

    print(a.shape)

    print(np.reshape(a, (1, 4)))     # 真实a没有变


def tf1():
    tf.InteractiveSession()
    a = tf.zeros((2, 2))
    print(a)
    b = tf.ones((2, 2))
    print(tf.reduce_sum(b, reduction_indices=1).eval())

    print(a.get_shape())
    print(tf.reshape(a, (1, 4)).eval())


def tf2():
    a = tf.constant(5.0)
    b = tf.constant(6.0)

    c = a * b

    with tf.Session() as sess:
        print(sess.run(c))
        print(c.eval())


def tf3():
    w1 = tf.ones((2, 2))

    w2 = tf.Variable(tf.zeros((2, 2)), name="weights")

    R = tf.Variable(tf.random_normal((2, 2)), name="random_weights")

    with tf.Session() as sess:
        print(sess.run(w1))
        sess.run(tf.global_variables_initializer())  # instead of initialize_all_variables
        print(sess.run(w2))
        print(sess.run(R))


def tf4():
    state = tf.Variable(0, name="counter")
    newstate = tf.add(state, tf.constant(1))
    update = tf.assign(state, newstate)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(state))
        for _ in range(3):
            sess.run(update)
            print(sess.run(state))


def tf5():
    input1 = tf.constant(3.0)
    input2 = tf.constant(2.0)
    input3 = tf.constant(5.0)
    intermed = tf.add(input2, input3)

    mul = tf.multiply(input1, intermed)
    with tf.Session() as sess:
        result = sess.run([mul, intermed])
        print(result)


def tf6():
    a = np.zeros((2, 2))
    t = tf.convert_to_tensor(a)
    with tf.Session() as sess:
        print(sess.run(t))


def tf7():
    input1 = tf.placeholder(tf.float32)
    input2 = tf.placeholder(tf.float32)

    output = tf.multiply(input1, input2)

    with tf.Session() as sess:
        print(sess.run([output], feed_dict={input1: [2, 1], input2: [2, 1]}))


def tf8():
    with tf.variable_scope("foo"):
        with tf.variable_scope("bar"):
            v = tf.get_variable("v", [1])
    assert v.name == "foo/bar/v:0"

    with tf.variable_scope("foo"):
        v = tf.get_variable("v", [1])
        # tf.get_variable_scope().reuse_variables()
        v1 = tf.get_variable("g", [1])
    print(v1)
    # assert v1 == v

    with tf.variable_scope("zoo", reuse=True):
        v = tf.get_variable("v", [1])


def tf9():
    X_data = np.arange(100, step=.1)
    y_data = X_data + 20 * np.sin(X_data / 10)
    n_samples = 1000
    batch_size = 100

    X_data = np.reshape(X_data, (n_samples, 1))
    y_data = np.reshape(y_data, (n_samples, 1))

    X = tf.placeholder(tf.float32, shape=(batch_size, 1))
    y = tf.placeholder(tf.float32, shape=(batch_size, 1))

    with tf.variable_scope("linear-regression"):
        W = tf.get_variable("weights", (1, 1), initializer=tf.random_normal_initializer())
        b = tf.get_variable("bias", (1,), initializer=tf.constant_initializer(0.0))
        y_pred = tf.matmul(X, W) + b
        loss = tf.reduce_sum((y - y_pred) ** 2 / n_samples)

    # opt = tf.train.AdamOptimizer()
    # opt_operation = opt.minimize(loss)
    # with tf.Session() as sess:
    #     sess.run(tf.global_variables_initializer())
    #     sess.run([opt_operation], feed_dict={X: X_data, y: y_data})

    opt_operation = tf.train.AdamOptimizer().minimize(loss)
    with tf.Session() as sess:
        # Initialize Variables in graph
        sess.run(tf.global_variables_initializer())
        # Gradient descent loop for 500 steps 自动梯度下降
        for _ in range(500):
            # Select random minibatch
            indices = np.random.choice(n_samples, batch_size)
            X_batch, y_batch = X_data[indices], y_data[indices]
            # Do gradient descent step
            _, loss_val = sess.run([opt_operation, loss], feed_dict={X: X_batch, y: y_batch})

    plt.scatter(X_data, y_data)
    plt.show()


def tf10():
    x = tf.truncated_normal((2, 2))
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(x))
