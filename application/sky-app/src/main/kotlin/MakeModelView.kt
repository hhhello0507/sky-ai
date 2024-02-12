//import androidx.compose.desktop.ui.tooling.preview.Preview
//import androidx.compose.foundation.layout.Column
//import androidx.compose.foundation.layout.Row
//import androidx.compose.material.Button
//import androidx.compose.material.OutlinedButton
//import androidx.compose.material.Text
//import androidx.compose.runtime.*
//import androidx.compose.ui.ExperimentalComposeUiApi
//import androidx.compose.ui.unit.dp
//import androidx.compose.ui.window.AwtWindow
//import androidx.compose.ui.window.DialogProperties
//import com.darkrockstudios.libraries.mpfilepicker.DirectoryPicker
//import java.awt.FileDialog
//import java.awt.Frame
//import java.io.BufferedReader
//import java.io.InputStreamReader
//
//@Composable
//@Preview
//fun MakeModelView() {
//    var showDirPicker1 by remember { mutableStateOf(false) }
//    var showDirPicker2 by remember { mutableStateOf(false) }
//    var folder1 by remember { mutableStateOf("") }
//    var folder2 by remember { mutableStateOf("") }
//
//    fun makeModel() {
//        // Python 스크립트 실행
//        val processBuilder = ProcessBuilder("python", "train.py", "product_name", "train_path")
//        val process = processBuilder.start()
//
//        // Python 스크립트의 출력을 읽어오기
//        val reader = BufferedReader(InputStreamReader(process.inputStream))
//        var line: String?
//        val output = StringBuilder()
//
//        while (reader.readLine().also { line = it } != null) {
//            output.append(line)
//        }
//
//        println("Python 스크립트의 출력: ${output.toString()}")
//    }
//
//    Column {
//        Title("정상 제품 이미지 경로")
//        Row {
//            Text(folder1)
//            OutlinedButton(onClick = {
//                showDirPicker1 = true
//            }) {
//                Text("찾아보기")
//            }
//        }
//        Title("불량 제품 이미지 경로")
//        Row {
//            Text(folder2)
//            OutlinedButton(onClick = {
//                showDirPicker2 = true
//            }) {
//                Text("찾아보기")
//            }
//        }
//        DirectoryPicker(showDirPicker1) { path ->
//            showDirPicker1 = false
//            folder1 = path?: ""
//        }
//        DirectoryPicker(showDirPicker2) { path ->
//            showDirPicker2 = false
//            folder2 = path?: ""
//        }
//        Button(onClick = {
//
//        }) {
//            Text("만들기")
//        }
//    }
//}
