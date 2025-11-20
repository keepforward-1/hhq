"""
星系分类模型训练脚本
使用Galaxy10 DECaLS数据集训练模型，目标精度89%
"""
import numpy as np
import h5py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, optimizers, callbacks
from sklearn.model_selection import train_test_split
import os

# 设置随机种子
np.random.seed(42)
tf.random.set_seed(42)

# 模型保存路径
MODEL_PATH = 'models/galaxy_classification_model.h5'
os.makedirs('models', exist_ok=True)

def load_galaxy10_data(data_path='Galaxy10_DECals.h5'):
    """
    加载Galaxy10 DECaLS数据集
    数据集可以从 https://astronn.readthedocs.io/en/latest/galaxy10.html 下载
    """
    print("正在加载数据集...")
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"数据集文件 {data_path} 不存在。\n"
            "请从以下链接下载Galaxy10 DECaLS数据集：\n"
            "https://astronn.readthedocs.io/en/latest/galaxy10.html"
        )
    
    with h5py.File(data_path, 'r') as F:
        images = np.array(F['images'])
        labels = np.array(F['ans'])
    
    print(f"数据集加载完成：{len(images)} 张图片")
    print(f"图片形状：{images.shape}")
    print(f"标签形状：{labels.shape}")
    print(f"类别数量：{len(np.unique(labels))}")
    
    return images, labels

def preprocess_data(images, labels):
    """预处理数据"""
    print("正在预处理数据...")
    
    # 归一化到[0, 1]
    images = images.astype('float32') / 255.0
    
    # 转换为one-hot编码
    num_classes = 10
    labels_one_hot = keras.utils.to_categorical(labels, num_classes)
    
    print(f"数据预处理完成")
    print(f"图片范围：[{images.min():.3f}, {images.max():.3f}]")
    
    return images, labels_one_hot

def build_model(input_shape=(69, 69, 3), num_classes=10):
    """
    构建CNN模型
    使用深度卷积神经网络，包含多个卷积层和全连接层
    """
    print("正在构建模型...")
    
    model = models.Sequential([
        # 第一组卷积层
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # 第二组卷积层
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # 第三组卷积层
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # 第四组卷积层
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # 展平
        layers.Flatten(),
        
        # 全连接层
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        
        # 输出层
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # 编译模型
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_3_accuracy']
    )
    
    print("模型构建完成")
    model.summary()
    
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
    """训练模型"""
    print("开始训练模型...")
    
    # 数据增强
    datagen = keras.preprocessing.image.ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1
    )
    datagen.fit(X_train)
    
    # 回调函数
    callbacks_list = [
        callbacks.ModelCheckpoint(
            MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # 训练
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=batch_size),
        steps_per_epoch=len(X_train) // batch_size,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=callbacks_list,
        verbose=1
    )
    
    return history

def evaluate_model(model, X_test, y_test):
    """评估模型"""
    print("正在评估模型...")
    
    test_loss, test_accuracy, test_top3_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\n测试集结果：")
    print(f"损失：{test_loss:.4f}")
    print(f"准确率：{test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"Top-3准确率：{test_top3_accuracy:.4f} ({test_top3_accuracy*100:.2f}%)")
    
    # 预测
    y_pred = model.predict(X_test, verbose=0)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    # 计算每个类别的准确率
    from sklearn.metrics import classification_report, confusion_matrix
    print("\n分类报告：")
    print(classification_report(y_true_classes, y_pred_classes))
    
    return test_accuracy

def main():
    """主函数"""
    print("=" * 60)
    print("星系分类模型训练")
    print("目标精度：89%")
    print("=" * 60)
    
    try:
        # 1. 加载数据
        images, labels = load_galaxy10_data()
        
        # 2. 预处理数据
        images, labels_one_hot = preprocess_data(images, labels)
        
        # 3. 划分数据集（70%训练，15%验证，15%测试）
        X_train, X_temp, y_train, y_temp = train_test_split(
            images, labels_one_hot, test_size=0.3, random_state=42, stratify=labels
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=np.argmax(y_temp, axis=1)
        )
        
        print(f"\n数据集划分：")
        print(f"训练集：{len(X_train)} 张")
        print(f"验证集：{len(X_val)} 张")
        print(f"测试集：{len(X_test)} 张")
        
        # 4. 构建模型
        model = build_model()
        
        # 5. 训练模型
        history = train_model(model, X_train, y_train, X_val, y_val, epochs=100, batch_size=32)
        
        # 6. 加载最佳模型
        if os.path.exists(MODEL_PATH):
            model = keras.models.load_model(MODEL_PATH)
            print(f"\n已加载最佳模型：{MODEL_PATH}")
        
        # 7. 评估模型
        accuracy = evaluate_model(model, X_test, y_test)
        
        # 8. 检查是否达到目标精度
        target_accuracy = 0.89
        if accuracy >= target_accuracy:
            print(f"\n✓ 模型训练成功！")
            print(f"  测试准确率：{accuracy*100:.2f}% >= 目标精度：{target_accuracy*100:.2f}%")
        else:
            print(f"\n⚠ 模型精度未达到目标")
            print(f"  测试准确率：{accuracy*100:.2f}% < 目标精度：{target_accuracy*100:.2f}%")
            print(f"  建议：增加训练轮数或调整模型结构")
        
        print(f"\n模型已保存至：{MODEL_PATH}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

