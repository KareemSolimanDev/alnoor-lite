let audio = document.querySelector('.quranPlayer'),
    surahsContainer = document.querySelector('.surahs'),
    ayah = document.querySelector('.ayah'),
    next = document.querySelector('.next'),
    prev = document.querySelector('.prev'),
    play = document.querySelector('.play');
    getSurahs();
    function getSurahs(){
    fetch('https://quran-endpoint.vercel.app/quran/')
    .then(response => response.json())
    .then(data=>{
        for(let text of data.data){
            surahsContainer.innerHTML+=`
            
            <div><h2>${text.asma.ar.long}</h2></div>
            `
        }
        let allSurahs = document.querySelectorAll('.surahs h2')
        allSurahs.forEach((s,i)=>{
            
            s.onclick=(e)=>{
        fetch(`https://quran-endpoint.vercel.app/quran/${i + 1}`)
        .then(response => response.json())
        .then(data=> {
            console.log(data);
                let ayahs =  data.data.ayahs;
                AyahsAudios = [];
                AyahsText = [];
                ayahs.forEach(ayah=>{
                    AyahsAudios.push(ayah.audio.url)
                    AyahsText.push(ayah.text.ar)
                })

                let AyahIndex = 0;
                changeAyah(AyahIndex)
                audio.addEventListener('ended',()=>{
                    AyahIndex++;
                    if(AyahIndex < AyahsAudios.length)
                    {
                        changeAyah(AyahIndex)
                    }
                    else
                    {
                        AyahIndex = 0;
                        changeAyah(AyahIndex);
                        audio.pause() 
                         isPlaying = true;
                         togglePlay()
                    }
                })
                //Handle Next And Prev
                 next.addEventListener('click',()=>{
                     AyahIndex < AyahsAudios.length - 1 ? AyahIndex++ : AyahIndex = 0;
                     changeAyah(AyahIndex)
                     isPlaying = false ;
                     togglePlay()
                 })
                 prev.addEventListener('click',()=>{
                     AyahIndex == 0 ? AyahIndex = AyahsAudios.length - 1 : AyahIndex--;
                     changeAyah(AyahIndex)
                     isPlaying = false ;
                     togglePlay()
                 })
                 //handle Play And Pause Audio
                 let isPlaying = false ;
                 togglePlay()
                 function togglePlay()
                 {
                     if(isPlaying)
                     {   
                        audio.pause();
                        play.innerHTML = `<i class="fas fa-play p-3 bg-mixed mx-2 rounded-circle text-white"></i>`;
                        isPlaying =false;
                     }
                     else
                     {
                         audio.play();
                         play.innerHTML = `<i class="fas fa-pause p-3 bg-mixed mx-2 rounded-circle text-white"></i>`;
                         isPlaying = true;
                     }
                    
                 }
                 play.addEventListener('click',togglePlay)
                function changeAyah(index)
                {
                     audio.src = AyahsAudios[index];
                     ayah.innerHTML = AyahsText[index]
                }


        })
            }
    })
        })
    }
