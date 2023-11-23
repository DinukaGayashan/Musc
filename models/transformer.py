import pickle
import time

import numpy as np
import tensorflow as tf
from dotenv import dotenv_values

from models import modules
from models import utils

from ui import utility


class PopMusicTransformer(object):

    def __init__(self, checkpoint, is_training=False, train_from_scratch=False):
        self.dictionary_path = utility.get_dictionary()
        self.event2word, self.word2event = pickle.load(
            open(self.dictionary_path, 'rb'))
        self.x_len = 512
        self.mem_len = 512
        self.n_layer = 12
        self.d_embed = 512
        self.d_model = 512
        self.dropout = 0.1
        self.n_head = 8
        self.d_head = self.d_model // self.n_head
        self.d_ff = 2048
        self.n_token = len(self.event2word)
        self.learning_rate = 0.0002
        self.is_training = is_training
        self.train_from_scratch = train_from_scratch
        self.batch_size = 1
        self.checkpoint_path = f"{checkpoint}/model"
        self.load_model()

    def load_model(self):
        tf.compat.v1.disable_eager_execution()
        self.x = tf.compat.v1.placeholder(
            tf.int32, shape=[self.batch_size, None])
        self.y = tf.compat.v1.placeholder(
            tf.int32, shape=[self.batch_size, None])
        self.mems_i = [tf.compat.v1.placeholder(tf.float32, [self.mem_len, self.batch_size, self.d_model]) for _ in
                       range(self.n_layer)]
        self.global_step = tf.compat.v1.train.get_or_create_global_step()
        initializer = tf.compat.v1.initializers.random_normal(
            stddev=0.02, seed=None)
        proj_initializer = tf.compat.v1.initializers.random_normal(
            stddev=0.01, seed=None)
        with tf.compat.v1.variable_scope(tf.compat.v1.get_variable_scope()):
            xx = tf.transpose(self.x, [1, 0])
            yy = tf.transpose(self.y, [1, 0])
            loss, self.logits, self.new_mem = modules.transformer(
                dec_inp=xx,
                target=yy,
                mems=self.mems_i,
                n_token=self.n_token,
                n_layer=self.n_layer,
                d_model=self.d_model,
                d_embed=self.d_embed,
                n_head=self.n_head,
                d_head=self.d_head,
                d_inner=self.d_ff,
                dropout=self.dropout,
                dropatt=self.dropout,
                initializer=initializer,
                proj_initializer=proj_initializer,
                is_training=self.is_training,
                mem_len=self.mem_len,
                cutoffs=[],
                div_val=-1,
                tie_projs=[],
                same_length=False,
                clamp_len=-1,
                input_perms=None,
                target_perms=None,
                head_target=None,
                untie_r=False,
                proj_same_dim=True)
        self.avg_loss = tf.reduce_mean(loss)
        all_vars = tf.compat.v1.trainable_variables()
        grads = tf.gradients(self.avg_loss, all_vars)
        grads_and_vars = list(zip(grads, all_vars))
        all_trainable_vars = tf.reduce_sum(
            [tf.reduce_prod(v.shape) for v in tf.compat.v1.trainable_variables()])
        decay_lr = tf.compat.v1.train.cosine_decay(
            self.learning_rate,
            global_step=self.global_step,
            decay_steps=400000,
            alpha=0.004)
        optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=decay_lr)
        self.train_op = optimizer.apply_gradients(
            grads_and_vars, self.global_step)
        self.saver = tf.compat.v1.train.Saver()
        config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
        config.gpu_options.allow_growth = True
        self.sess = tf.compat.v1.Session(config=config)
        if self.train_from_scratch:
            self.sess.run(tf.compat.v1.global_variables_initializer())
        else:
            self.saver.restore(self.sess, self.checkpoint_path)

    def temperature_sampling(self, logits, temperature, topk):
        probs = np.exp(logits / temperature) / \
            np.sum(np.exp(logits / temperature))
        if topk == 1:
            prediction = np.argmax(probs)
        else:
            sorted_index = np.argsort(probs)[::-1]
            candi_index = sorted_index[:topk]
            candi_probs = [probs[i] for i in candi_index]
            candi_probs /= sum(candi_probs)
            prediction = np.random.choice(
                candi_index, size=1, p=candi_probs)[0]
        return prediction

    def extract_events(self, input_path):
        note_items, tempo_items = utils.read_items(input_path)
        note_items = utils.quantize_items(note_items)
        max_time = note_items[-1].end
        if 'chord' in self.checkpoint_path:
            chord_items = utils.extract_chords(note_items)
            items = chord_items + tempo_items + note_items
        else:
            items = tempo_items + note_items
        groups = utils.group_items(items, max_time)
        events = utils.item2event(groups)
        return events

    def generate(self, name, n_target_bar, temperature):
        words = []
        for _ in range(self.batch_size):
            ws = [self.event2word['Bar_None']]
            if 'chord' in self.checkpoint_path:
                tempo_classes = [
                    v for k, v in self.event2word.items() if 'Tempo Class' in k]
                tempo_values = [
                    v for k, v in self.event2word.items() if 'Tempo Value' in k]
                chords = [v for k, v in self.event2word.items()
                          if 'Chord' in k]
                ws.append(self.event2word['Position_1/16'])
                ws.append(np.random.choice(chords))
                ws.append(self.event2word['Position_1/16'])
                ws.append(np.random.choice(tempo_classes))
                ws.append(np.random.choice(tempo_values))
            else:
                tempo_classes = [
                    v for k, v in self.event2word.items() if 'Tempo Class' in k]
                tempo_values = [
                    v for k, v in self.event2word.items() if 'Tempo Value' in k]
                ws.append(self.event2word['Position_1/16'])
                ws.append(np.random.choice(tempo_classes))
                ws.append(np.random.choice(tempo_values))
            words.append(ws)
        batch_m = [np.zeros((self.mem_len, self.batch_size, self.d_model), dtype=np.float32) for _ in
                   range(self.n_layer)]
        original_length = len(words[0])
        initial_flag = 1
        current_generated_bar = 0
        while current_generated_bar < n_target_bar:
            if initial_flag:
                temp_x = np.zeros((self.batch_size, original_length))
                for b in range(self.batch_size):
                    for z, t in enumerate(words[b]):
                        temp_x[b][z] = t
                initial_flag = 0
            else:
                temp_x = np.zeros((self.batch_size, 1))
                for b in range(self.batch_size):
                    temp_x[b][0] = words[b][-1]
            feed_dict = {self.x: temp_x}
            for m, m_np in zip(self.mems_i, batch_m):
                feed_dict[m] = m_np
            _logits, _new_mem = self.sess.run(
                [self.logits, self.new_mem], feed_dict=feed_dict)
            _logit = _logits[-1, 0]
            word = self.temperature_sampling(
                logits=_logit,
                temperature=temperature,
                topk=5)
            words[0].append(word)
            if word == self.event2word['Bar_None']:
                current_generated_bar += 1
            batch_m = _new_mem
        utils.write_midi(
            name=name,
            words=words[0],
            word2event=self.word2event)

    def prepare_data(self, midi_paths):
        all_events = []
        for path in midi_paths:
            events = self.extract_events(path)
            all_events.append(events)
        all_words = []
        for events in all_events:
            words = []
            for event in events:
                e = '{}_{}'.format(event.name, event.value)
                if e in self.event2word:
                    words.append(self.event2word[e])
                else:
                    if event.name == 'Note Velocity':
                        words.append(self.event2word['Note Velocity_21'])
                    else:
                        print('something is wrong! {}'.format(e))
            all_words.append(words)
        self.group_size = 5
        segments = []
        for words in all_words:
            pairs = []
            for i in range(0, len(words) - self.x_len - 1, self.x_len):
                x = words[i:i + self.x_len]
                y = words[i + 1:i + self.x_len + 1]
                pairs.append([x, y])
            pairs = np.array(pairs)
            for i in np.arange(0, len(pairs) - self.group_size, self.group_size * 2):
                data = pairs[i:i + self.group_size]
                if len(data) == self.group_size:
                    segments.append(data)
        segments = np.array(segments)
        return segments

    def finetune(self, training_data, output_checkpoint_folder):
        index = np.arange(len(training_data))
        np.random.shuffle(index)
        training_data = training_data[index]
        num_batches = len(training_data) // self.batch_size
        st = time.time()
        for e in range(10):
            total_loss = []
            for i in range(num_batches):
                segments = training_data[self.batch_size *
                                         i:self.batch_size * (i + 1)]
                batch_m = [np.zeros((self.mem_len, self.batch_size, self.d_model), dtype=np.float32) for _ in
                           range(self.n_layer)]
                for j in range(self.group_size):
                    batch_x = segments[:, j, 0, :]
                    batch_y = segments[:, j, 1, :]
                    feed_dict = {self.x: batch_x, self.y: batch_y}
                    for m, m_np in zip(self.mems_i, batch_m):
                        feed_dict[m] = m_np
                    _, gs_, loss_, new_mem_ = self.sess.run(
                        [self.train_op, self.global_step, self.avg_loss, self.new_mem], feed_dict=feed_dict)
                    batch_m = new_mem_
                    total_loss.append(loss_)
                    print('>>> Epoch: {}, Step: {}, Loss: {:.5f}, Time: {:.2f}'.format(
                        e, gs_, loss_, time.time() - st))
            self.saver.save(
                self.sess, '{}/model'.format(output_checkpoint_folder, e, np.mean(total_loss)))
            if np.mean(total_loss) <= 0.1:
                break

    def close(self):
        self.sess.close()
