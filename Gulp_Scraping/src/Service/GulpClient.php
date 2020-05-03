<?php


namespace App\Service;


use Symfony\Component\HttpClient\HttpClient;
use Symfony\Contracts\HttpClient\HttpClientInterface;
use Symfony\Component\Dotenv\Dotenv;

/**
 * Class FreelancerMapClient
 *
 * @package App\Service
 */
class GulpClient
{

    private const GULP_OAUTH_TOKEN_URL = "https://www.gulp.de/direkt/app/oauth/token";

    /**
     * @var HttpClient
     */
    private $client;

    /**
     * @var boolean
     */
    private $loggedIn;

    /**
     * FreelancerMapClient constructor.
     */
    public function __construct()
    {
        $this->client = HttpClient::create(['timeout' => 60,
            'headers' => [
                'Accept' => 'application/json'
            ]]);

        $dotenv = new Dotenv();
        $dotenv->loadEnv('.env');
    }

    /**
     * @return HttpClientInterface
     */
    public function getClient(): HttpClientInterface
    {
        return $this->client;
    }

    public function login()
    {
        if (!$this->loggedIn) {
            $loginResult = $this->client->request('POST', self::GULP_OAUTH_TOKEN_URL, [
                'body' => [
                    'grant_type' => 'password',
                    'username' => $_ENV['USER_NAME'],
                    'password' => $_ENV['PASSWORD']
                ],
                'headers' => [
                    'Authorization' => 'Basic ZGlyZWt0LWNsaWVudDpzZWNyZXQ='
                ]
            ]);

            $response = json_decode($loginResult->getContent(), true);
            $this->client = HttpClient::create(['timeout' => 60,
                'headers' => [
                    'Accept' => 'application/json',
                    'Content-Type' => 'application/json',
                    'Authorization' => "Bearer " . $response['access_token']
                ]]);
        }
    }

}