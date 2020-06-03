<?php
//if (isset($_FILES["postImage"]["name"])){
   session_start();
        if( isset($_POST["postCategory"]) &&
            isset($_POST["postTitle"]) &&    
            isset($_POST["postBody"])){
                
                //post data
                $userId = $_SESSION["user_id"];
                $postCategory = $_POST["postCategory"];
                $postTitle = $_POST["postTitle"];
                $postBody = $_POST["postBody"];
                    
                //image data
                $fileName = $_FILES["postImage"]["name"];
                
                $fileTmpLoc = $_FILES["postImage"]["tmp_name"];
                $fileType = $_FILES["postImage"]["type"];
                $fileSize = $_FILES["postImage"]["size"];
                $fileErrorMsg = $_FILES["postImage"]["error"];
                $kaboom = explode(".", $fileName);
                $fileExt = end($kaboom);

                //image upload fail conditions
                if($fileSize > 597152){
                    echo "<script> alert('Upload Failed|Your image file was larger than 5mb')</script>";
                    //exit();
                }
                if (!preg_match("/.(gif||png||jpg||jpeg)$/i", $fileExt)){
                    echo "<script> alert('Your file was not JPG, GIF or PNG type')</script>";
                    //exit();
                }
                if ($fileErrorMsg == 1) {
                    echo "<script> alert('An unknown error occurred')</script>";
                   //exit();
                }
            
                $db_file_name = generateRandomString(5).".".$fileExt;//random file name
                if(isset($_POST["postBody"]){

                }
                if (move_uploaded_file($fileTmpLoc, "post_images/$db_file_name")) {
                        
                    require('connect.php');

                    $sql = "INSERT INTO `posts`(`user_id`, `category`, `title`, `body`, `images`, `post_time`, `num_likes`, `num_dislikes`, `num_comments`) VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)";
                    $stmt = $pdo->prepare($sql);

                    $stmt->execute([$userId , $postCategory, $postTitle, $postBody, $db_file_name, 0, 0, 0, 0]);

                    if($stmt){
                        echo "<script> alert('Post Sent Sucessfully')</script>";
                    }
                    else{
                        echo "<script> alert('Failed | Unknown Error Occurred ')</script>";
                    }
                } else {
                    echo "<script> alert('Error')</script>";
                }   
               // header('Location: createPost.php');
                
        }
        function generateRandomString($length = 10) {
            $r1 = uniqid("PostImage");
            $characters = '0123456789';
            $charactersLength = strlen($characters);
            $randomString = '';
            for ($i = 0; $i < $length; $i++) {
                $randomString .= $characters[rand(0, $charactersLength - 1)];
            }
            return $randomString; 
        }
   // }
?>

