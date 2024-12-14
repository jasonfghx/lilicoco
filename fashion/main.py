import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# 定義激活函數
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))#keepdims用於保持同樣長度
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# 定義交叉熵損失函數
def cross_entropy_loss(y_true, y_pred):
    m = y_true.shape[0]
    log_likelihood = -np.log(y_pred[range(m), y_true.argmax(axis=1)])
    loss = np.sum(log_likelihood) / m
    return loss

# 隨機初始化權重和偏置
def initialize_weights(input_size, hidden_size_1, hidden_size_2, output_size):
    W1 = np.random.randn(input_size, hidden_size_1) * 0.01 # 第一層權重
    b1 = np.zeros((1, hidden_size_1))
    W2 = np.random.randn(hidden_size_1, hidden_size_2) * 0.01 # 第二層權重
    b2 = np.zeros((1, hidden_size_2))
    W3 = np.random.randn(hidden_size_2, output_size) * 0.01 # 輸出層權重
    b3 = np.zeros((1, output_size))

    return W1, b1, W2, b2, W3, b3

# 前向傳播計算
def forward(X, W1, b1, W2, b2, W3, b3):
    Z1 = np.dot(X, W1) + b1  # 第一層線性變換
    A1 = relu(Z1)  # 第一層activation 
    Z2 = np.dot(A1, W2) + b2  # 第二層線性變換
    A2 = relu(Z2)  # 第二層activation 
    Z3 = np.dot(A2, W3) + b3  # 輸出層線性變換
    A3 = softmax(Z3)  # 輸出層activation 
    return A1, A2, A3

# 反向傳播
def backward(X, y, A1, A2, A3, W1, W2, W3):
    m = X.shape[0]

    # 計算輸出層的梯度
    dZ3 = A3 - y
    dW3 = np.dot(A2.T, dZ3) / m
    db3 = np.sum(dZ3, axis=0, keepdims=True) / m # 輸出層梯度

    dA2 = np.dot(dZ3, W3.T) # 傳遞回第二層
    dZ2 = dA2 * relu_derivative(A2) # 第二層梯度
    dW2 = np.dot(A1.T, dZ2) / m # 第二層權重梯度
    db2 = np.sum(dZ2, axis=0, keepdims=True) / m # 輸出層梯度

    dA1 = np.dot(dZ2, W2.T) # 傳遞回第一層
    dZ1 = dA1 * relu_derivative(A1) # 第一層梯度
    dW1 = np.dot(X.T, dZ1) / m # 第一層權重梯度
    db1 = np.sum(dZ1, axis=0, keepdims=True) / m # 輸出層梯度

    return dW1, db1, dW2, db2, dW3, db3

# 更新模型參數
def update_parameters(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, learning_rate):
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    W3 -= learning_rate * dW3
    b3 -= learning_rate * db3

    return W1, b1, W2, b2, W3, b3

# 訓練模型
def train(X_train, y_train,X_test,y_test, input_size, hidden_size_1, hidden_size_2, output_size, batch_size, epochs, learning_rate):
  W1, b1, W2, b2, W3, b3 = initialize_weights(input_size, hidden_size_1, hidden_size_2, output_size)
  loss_l,loss_v_l=[],[]
  for epoch in range(epochs):

        # 隨機打亂訓練數據
    perm = np.random.permutation(X_train.shape[0])
    X_train = X_train[perm]
    y_train = y_train[perm]

    for i in range(0, X_train.shape[0], batch_size): # 隨機打亂訓練數據

            # Mini-Batch 分批處理
      X_batch = X_train[i:i+batch_size]
      y_batch = y_train[i:i+batch_size]

            # 前向傳播
      A1, A2, A3 = forward(X_batch, W1, b1, W2, b2, W3, b3)
      A1_v, A2_v, A3_v = forward(X_test, W1, b1, W2, b2, W3, b3)
            # 計算損失
      loss = cross_entropy_loss(y_batch, A3)
      loss_v = cross_entropy_loss(y_test, A3_v)
            # 反向傳播
      dW1, db1, dW2, db2, dW3, db3 = backward(X_batch, y_batch, A1, A2, A3, W1, W2, W3)

            # 更新權重
      W1, b1, W2, b2, W3, b3 = update_parameters(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, learning_rate)
      loss_l.append(loss)
      loss_v_l.append(loss_v)
        # 每隔一段時間輸出一次損失
      if (epoch + 1) % 10 == 0:
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss}')
        print(f'Epoch {epoch+1}/{epochs}, Val Loss: {loss_v}')

  return W1, b1, W2, b2, W3, b3,loss_l,loss_v_l

# 假設輸入數據是 X_train 和 One-Hot 編碼的標籤是 y_train
input_size = 784  # 輸入層大小
hidden_size1 = 128  # 第一層隱藏層大小
hidden_size2 = 64   # 第二層隱藏層大小
output_size = 10
batch_size = 128
epochs = 20
learning_rate = 0.01

script_dir = os.path.dirname(os.path.abspath(__file__))  # 獲取當前程式檔案路徑
train_file_path = os.path.join(script_dir, 'train.csv')  # 設定訓練檔案路徑
test_file_path = os.path.join(script_dir, 'test.csv')  # 設定測試檔案路徑
X_train = np.array(pd.read_csv(train_file_path).iloc[:15000,1:])
y_train = pd.read_csv(train_file_path).iloc[:15000,0]
X_test = np.array(pd.read_csv(train_file_path).iloc[15000:,1:])
y_test = pd.read_csv(train_file_path).iloc[15000:,0]

y_train = np.eye(10)[y_train]  # 轉換為 One-Hot 編碼
y_test= np.eye(10)[y_test]
# 訓練模型
W1, b1,W2,b2,W3,b3,loss_l,loss_v_l = train(X_train, y_train,X_test,y_test, input_size, hidden_size1, hidden_size2, output_size, batch_size, epochs, learning_rate)
plt.plot(list(range(0,len(loss_l))), loss_l, label='train', color='b')  # b是藍色
plt.plot(list(range(0,len(loss_v_l))), loss_v_l, label='val', color='r')  # r是紅色

# 添加標題和標籤
plt.title('LOSS')
plt.xlabel('EPOCH')
plt.ylabel('LOSS')

# 顯示圖例
plt.legend()
output_image_path = os.path.join(script_dir, "output.png")

plt.savefig(output_image_path)
# 計算測試專用
def forward_pre(X, W1, b1, W2, b2, W3, b3):
    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)

    Z2 = np.dot(A1, W2) + b2
    A2 = relu(Z2)

    Z3 = np.dot(A2, W3) + b3
    A3 = softmax(Z3)

    return A3
pre=[]
pre_data=pd.read_csv(test_file_path)
for i in range(0,pre_data.shape[0]):
  A3 = forward_pre(pre_data.iloc[i,:], W1, b1, W2, b2, W3, b3)
  predicted_class = np.argmax(A3, axis=1)
  pre.append(predicted_class[0])
output_path = os.path.join(script_dir, "test_output.txt")  
with open(output_path, 'w') as file:
  for item in pre:
    file.write(str(item) + '\n')  
print('Layers:',2)
print('Each layer neurons:')
print('Layer1',hidden_size1)
print('Layer2',hidden_size2)
print('Max Epoch:',epochs)
print('learning rate:',learning_rate)
print('batch size:',batch_size)

# train ACC
pre=[]
for i in range(0,X_train.shape[0]):
  A3 = forward_pre(X_train[i,:], W1, b1, W2, b2, W3, b3)
  predicted_class = np.argmax(A3, axis=1)
  pre.append(predicted_class[0])
y_train1=  np.argmax(y_train, axis=1)
accuracy = np.mean(y_train1 == pre)

print(f'Train Accuracy: {accuracy:.2f}')

pre=[]
for i in range(0,X_test.shape[0]):
  A3 = forward_pre(X_test[i,:], W1, b1, W2, b2, W3, b3)
  predicted_class = np.argmax(A3, axis=1)
  pre.append(predicted_class[0])
y_test=  np.argmax(y_test, axis=1)
accuracy = np.mean(y_test == pre)

print(f'Val Accuracy: {accuracy:.2f}')