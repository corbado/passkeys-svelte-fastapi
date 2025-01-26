<script>
	import '../main.css';
	import Navigation from '../components/Navigation.svelte';
	import Footer from '../components/Footer.svelte';
</script>

<Navigation />
<main>
	<section>
		<slot />
	</section>
	<Footer />
</main>
