import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.material.Button
import androidx.compose.material.Text
import androidx.compose.runtime.*
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.AwtWindow
import androidx.compose.ui.window.DialogProperties
import com.darkrockstudios.libraries.mpfilepicker.DirectoryPicker
import java.awt.FileDialog
import java.awt.Frame

@Composable
@Preview
fun MakeModelView() {
    var showDirPicker1 by remember { mutableStateOf(false) }
    var showDirPicker2 by remember { mutableStateOf(false) }
    var folder1 by remember { mutableStateOf("") }
    var folder2 by remember { mutableStateOf("") }
    Column {
        Title("정상 제품 이미지 경로")
        Row {
            Text(folder1)
            Button(onClick = {
                showDirPicker1 = true
            }) {
                Text("찾아보기")
            }
        }
        Title("불량 제품 이미지 경로")
        Row {
            Text(folder2)
            Button(onClick = {
                showDirPicker2 = true
            }) {
                Text("찾아보기")
            }
        }
        DirectoryPicker(showDirPicker1) { path ->
            showDirPicker1 = false
            folder1 = path?: ""
        }
        DirectoryPicker(showDirPicker2) { path ->
            showDirPicker2 = false
            folder2 = path?: ""
        }
        Button(onClick = {
            
        }) {
            Text("만들기")
        }
    }
}
